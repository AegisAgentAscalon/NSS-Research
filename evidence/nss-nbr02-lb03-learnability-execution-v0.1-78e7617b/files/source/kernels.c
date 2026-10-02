#include <stdint.h>
#include <math.h>
/* Block-local scratch only. Wider master and gradients are caller-owned. */
int adam_step(int n,float *p,const float *g,float *m,float *v,int8_t *qm,uint8_t *qv,float *sm,float *sv,int mode,int step,float lr){
 const float b1=.9f,b2=.999f; const double c1=1.-pow(.9,step),c2=1.-pow(.999,step);
 for(int start=0;start<n;start+=128){
  int len=n-start<128?n-start:128,bi=start/128;float mm[128],vv[128],mx=0.,vx=0.;
  for(int j=0;j<len;j++){
   int i=start+j;float om=mode?((float)qm[i]*sm[bi]):m[i];float ov;
   if(mode){float r=(float)qv[i]*sv[bi];ov=r*r;}else ov=v[i];
   /* Constants are exact decimal double expressions then cast to float state. */
   mm[j]=(float)(.9*(double)om+.1*(double)g[i]);
   vv[j]=(float)(.999*(double)ov+.001*(double)g[i]*(double)g[i]);
   double upd=((double)mm[j]/c1)/(sqrt((double)vv[j]/c2)+1e-8);
   p[i]=(float)((double)p[i]-(double)lr*upd);
   if(!isfinite(p[i])||!isfinite(mm[j])||!isfinite(vv[j])||vv[j]<0)return 1;
   if(fabsf(mm[j])>mx)mx=fabsf(mm[j]);if(vv[j]>vx)vx=vv[j];
   if(!mode){m[i]=mm[j];v[i]=vv[j];}
  }
  if(mode){
   sm[bi]=mx==0?0:mx/127.f;sv[bi]=vx==0?0:(float)(sqrt((double)vx)/255.);
   for(int j=0;j<len;j++){
    double am=sm[bi]?nearbyint((double)mm[j]/sm[bi]):0;
    double av=sv[bi]?nearbyint(sqrt((double)vv[j])/sv[bi]):0;
    if(am>127)am=127;if(am< -127)am=-127;if(av>255)av=255;if(av<0)av=0;
    qm[start+j]=(int8_t)am;qv[start+j]=(uint8_t)av;
   }
  }
 }
 return 0;
}
static inline double weight(const uint8_t *p,const float*s,const uint8_t*z,int row,int col,int cols){int j=row*cols+col;int code=(p[j/4]>>(2*(j%4)))&3;return (double)(float)((code-(int)z[row])*s[row]);}
/* Direct packed-code recurrent inference; no persistent dense weight expansion. */
void q2_rollout(int batch,int steps,const int64_t*t,const double*h0,
 const uint8_t*pi,const uint8_t*ph,const uint8_t*po,
 const float*si,const float*sh,const float*so,const uint8_t*zi,const uint8_t*zh,const uint8_t*zo,
 const float*bi,const float*bh,const float*bo,double*hs,double*out){
 for(int b=0;b<batch;b++){
  double h[64],nh[64];for(int k=0;k<64;k++)h[k]=h0[b*64+k];
  for(int j=0;j<steps;j++){
   int token=t[b*steps+j];double x[192],y[192];
   for(int r=0;r<192;r++){x[r]=weight(pi,si,zi,r,token,26)+bi[r];double s=bh[r];for(int k=0;k<64;k++)s+=weight(ph,sh,zh,r,k,64)*h[k];y[r]=s;}
   for(int k=0;k<64;k++){double rr=1./(1.+exp(-x[k]-y[k]));double zz=1./(1.+exp(-x[k+64]-y[k+64]));double nn=tanh(x[k+128]+rr*y[k+128]);nh[k]=(1.-zz)*nn+zz*h[k];}
   for(int k=0;k<64;k++){h[k]=nh[k];hs[(b*steps+j)*64+k]=h[k];}
   for(int r=0;r<9;r++){double s=bo[r];for(int k=0;k<64;k++)s+=weight(po,so,zo,r,k,64)*h[k];out[(b*steps+j)*9+r]=s;}
  }
 }
}
