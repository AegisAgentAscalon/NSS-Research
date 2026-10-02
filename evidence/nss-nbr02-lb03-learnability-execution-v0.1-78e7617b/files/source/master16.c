/* NSS LB02-MASTER16. FP16 matrix masters without a persistent FP32 shadow.
   Update arithmetic and gradient input stay wide. No fast-math; IEEE round-to-nearest.
   Moment format is the inherited custom signed m / square-root v SQ8 scheme. */
#include <stdint.h>
#include <string.h>
#include <math.h>
#include <float.h>
static float hload(const uint16_t *p,int i){_Float16 h;memcpy(&h,p+i,2);return (float)h;}
static uint16_t hround(float x){_Float16 h=(_Float16)x;uint16_t b;memcpy(&b,&h,2);return b;}
static float hbits(uint16_t b){return hload(&b,0);}
static uint16_t hup(uint16_t b){if((b&0x7fff)==0)return 1;return (b&0x8000)?b-1:b+1;}
static uint16_t hdown(uint16_t b){if((b&0x7fff)==0)return 0x8001;return (b&0x8000)?b+1:b-1;}
static uint64_t draw(uint64_t *s){uint64_t z=(*s+=UINT64_C(0x9e3779b97f4a7c15));z=(z^(z>>30))*UINT64_C(0xbf58476d1ce4e5b9);z=(z^(z>>27))*UINT64_C(0x94d049bb133111eb);return z^(z>>31);}
static uint16_t hrand(float x,uint64_t *s){double u=(draw(s)>>11)*0x1.0p-53;uint16_t near=hround(x);float y=hbits(near);if(y==x)return near;uint16_t lo=y>x?hdown(near):near,hi=y<x?hup(near):near;double l=hbits(lo),h=hbits(hi);return u<((double)x-l)/(h-l)?hi:lo;}
int round_array(int n,const float*x,uint16_t*out,int stochastic,uint64_t *s){for(int i=0;i<n;i++){if(!isfinite(x[i])||fabsf(x[i])>65504.f)return 1;out[i]=stochastic?hrand(x[i],s):hround(x[i]);}return 0;}
/* Exact row-specific affine four-code quantizer. Only a 64-float row scratch. */
int q2_effective(int rows,int cols,const void *raw,int half,float*out,uint8_t *codes,float *scales,uint8_t *zeros){
 if(cols>64||cols<1||rows<1)return 2;
 for(int r=0;r<rows;r++){float vals[64],lo=0.f,hi=0.f;
  for(int c=0;c<cols;c++){float w=half?hload((const uint16_t*)raw,r*cols+c):((const float*)raw)[r*cols+c];if(!isfinite(w))return 1;vals[c]=w;if(w<lo)lo=w;if(w>hi)hi=w;}
  float sc=(float)(((double)hi-(double)lo)/3.);if(sc<1e-8f)sc=1e-8f;
  float zero=nearbyintf(-lo/sc);if(zero<0)zero=0;if(zero>3)zero=3;scales[r]=sc;zeros[r]=(uint8_t)zero;
  for(int c=0;c<cols;c++){float q=nearbyintf(vals[c]/sc)+zero;if(q<0)q=0;if(q>3)q=3;codes[r*cols+c]=(uint8_t)q;out[r*cols+c]=(q-zero)*sc;}
 }return 0;
}
/* stats: intended f32 changes, stored changes, rounded-away changes, nonzero
   gradients, squared rounding error scaled separately via the double result. */
int adam_m8(int n,void *raw,const float*g,int half,int stochastic,int8_t *qm,uint8_t*qv,float*sm,float*sv,int step,float lr,uint64_t*rng,uint64_t*stats,double*rounderr){
 const double c1=1.-pow(.9,step),c2=1.-pow(.999,step);
 for(int start=0;start<n;start+=128){int len=n-start<128?n-start:128,b=start/128;float mm[128],vv[128],mx=0.f,vx=0.f;
  for(int j=0;j<len;j++){int i=start+j;float old=half?hload((uint16_t*)raw,i):((float*)raw)[i];float om=(float)qm[i]*sm[b],vroot=(float)qv[i]*sv[b],ov=vroot*vroot;
   if(!isfinite(old)||!isfinite(g[i]))return 1;
   mm[j]=(float)(.9*(double)om+.1*(double)g[i]);vv[j]=(float)(.999*(double)ov+.001*(double)g[i]*(double)g[i]);
   double delta=((double)mm[j]/c1)/(sqrt((double)vv[j]/c2)+1e-8);
   float x=(float)((double)old-(double)lr*delta);
   if(!isfinite(x)||!isfinite(mm[j])||!isfinite(vv[j])||vv[j]<0||(half&&fabsf(x)>65504.f))return 1;
   if(half)((uint16_t*)raw)[i]=stochastic?hrand(x,rng):hround(x);else ((float*)raw)[i]=x;
   float stored=half?hload((uint16_t*)raw,i):x;
   stats[0]+=(x!=old);stats[1]+=(stored!=old);stats[2]+=(x!=old&&stored==old);stats[3]+=(g[i]!=0.f);double er=(double)stored-x;rounderr[0]+=er*er;
   if(fabsf(mm[j])>mx)mx=fabsf(mm[j]);if(vv[j]>vx)vx=vv[j];
  }
  sm[b]=mx==0?0:mx/127.f;sv[b]=vx==0?0:(float)(sqrt((double)vx)/255.);
  for(int j=0;j<len;j++){double am=sm[b]?nearbyint((double)mm[j]/sm[b]):0,av=sv[b]?nearbyint(sqrt((double)vv[j])/sv[b]):0;if(am>127)am=127;if(am< -127)am=-127;if(av>255)av=255;if(av<0)av=0;qm[start+j]=(int8_t)am;qv[start+j]=(uint8_t)av;}
 }return 0;
}
