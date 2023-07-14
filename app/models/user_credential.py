import uuid

from sqlalchemy import CheckConstraint
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import LargeBinary
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Session
from sqlalchemy.orm import backref
from sqlalchemy.orm import relationship
from webauthn.registration.verify_registration_response import VerifiedRegistration

from app.db.base_class import Base
from app.models import User


class UserCredential(Base):
    """User Credential model."""

    __tablename__ = "user_credential"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    public_key = Column(LargeBinary(), nullable=False)
    credential_id = Column(LargeBinary(), nullable=False)
    sign_count = Column(Integer(), CheckConstraint("sign_count >= 0"), default=0)

    user = relationship(
        "User", backref=backref("credentials", uselist=False, passive_deletes=True), foreign_keys=[user_id]
    )

    @classmethod
    def create_credential(cls, db: Session, user: User, registration_data: VerifiedRegistration) -> "UserCredential":
        """Create user credential."""
        user_credential: UserCredential = cls(
            user_id=user.id,
            public_key=registration_data.credential_public_key,
            credential_id=registration_data.credential_id,
        )
        db.add(user_credential)
        db.commit()
        return user_credential

    def update_sign_count(self, db: Session, sign_count: int) -> None:
        """Increment sign count."""
        self.sign_count = sign_count
        db.add(self)
        db.commit()
