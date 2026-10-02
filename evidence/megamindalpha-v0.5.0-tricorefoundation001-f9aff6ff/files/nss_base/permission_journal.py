"""Permission-specific policy over shared local journal mechanics.

The public class and database format remain unchanged. Generation release uses a
separate subclass/store, not this replay permission policy.
"""
import secrets
from .local_journal import EventJournal, document, fault
from .permission_contracts import FORMAT, MAX_EVENTS, MAX_HISTORY_BYTES, POLICY_HASH, manifest


class PermissionJournal(EventJournal):
    filename = 'permissions.sqlite3'
    validate_manifest = staticmethod(manifest)
    max_events = MAX_EVENTS
    max_history_bytes = MAX_HISTORY_BYTES

    @classmethod
    def create(cls, directory, operators):
        return cls.create_document(directory, {
            'schema_version': 1, 'format': FORMAT, 'store_id': secrets.token_hex(16),
            'policy_sha256': POLICY_HASH, 'operators': operators})
