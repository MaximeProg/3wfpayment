import uuid
from datetime import datetime
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


class PersonInfo(BaseModel):
    """KYC minimal transmis a Yellow Card (recipient pour un depot, sender pour un
    retrait). Champs requis selon customer_type - cf. doc Yellow Card Submit
    Receive/Send Request.

    Yellow Card attend ces champs en camelCase (idType/idNumber/businessId/
    businessName) - les alias ci-dessous serialisent correctement vers Yellow
    Card (via model_dump(by_alias=True)) tout en acceptant en entree soit le nom
    Python (snake_case, deja utilise par les projets appelants existants) soit
    l'alias, grace a populate_by_name=True.
    """

    model_config = ConfigDict(populate_by_name=True)

    name: str | None = None
    country: str | None = Field(None, description="ISO 3166, ex: NG, CM, GH")
    phone: str | None = None
    address: str | None = None
    dob: str | None = Field(None, description="mm/dd/yyyy")
    email: str | None = None
    id_number: str | None = Field(None, alias="idNumber")
    id_type: str | None = Field(None, alias="idType")
    business_id: str | None = Field(None, alias="businessId")
    business_name: str | None = Field(None, alias="businessName")


class DepositCreateRequest(BaseModel):
    client_reference: str = Field(..., description="Idempotency key propre au projet appelant")
    customer_uid: str = Field(..., description="Identifiant du client dans le systeme du projet appelant")
    customer_type: Literal["retail", "institution"] = "retail"

    local_amount: Decimal = Field(..., gt=0, description="Montant en devise locale (sans decimales)")
    currency: str = Field(..., description="Code devise ISO 4217, ex: NGN, XAF")
    channel_id: uuid.UUID = Field(
        ..., description="Identifiant du channel (voir GET /v1/channels, ramp_type=deposit)"
    )

    source_account_type: Literal["bank", "momo"]
    source_account_number: str = Field(..., description="Numero de compte/telephone du payeur")
    source_network_id: uuid.UUID | None = Field(None, description="Requis pour momo (voir GET /v1/networks)")

    recipient: PersonInfo = Field(..., description="KYC du destinataire (le titulaire du wallet)")
    reason: str = "other"
    force_accept: bool = True

    @field_validator("local_amount")
    @classmethod
    def _no_decimals(cls, v: Decimal) -> Decimal:
        if v != v.to_integral_value():
            raise ValueError("local_amount doit etre un montant entier (pas de decimales) pour Yellow Card")
        return v


class WithdrawalCreateRequest(BaseModel):
    client_reference: str = Field(..., description="Idempotency key propre au projet appelant")
    customer_uid: str = Field(..., description="Identifiant du client dans le systeme du projet appelant")
    customer_type: Literal["retail", "institution"] = "retail"

    local_amount: Decimal = Field(..., gt=0, description="Montant en devise locale (sans decimales)")
    currency: str = Field(..., description="Code devise ISO 4217, ex: NGN, XAF")
    channel_id: uuid.UUID = Field(
        ..., description="Identifiant du channel (voir GET /v1/channels, ramp_type=withdraw)"
    )
    reason: str

    destination_account_type: Literal["bank", "momo"]
    destination_account_number: str
    destination_account_name: str
    destination_network_id: uuid.UUID | None = Field(None, description="Requis pour momo (voir GET /v1/networks)")

    sender: PersonInfo = Field(..., description="KYC de l'expediteur (le titulaire du wallet)")
    force_accept: bool = True

    @field_validator("local_amount")
    @classmethod
    def _no_decimals(cls, v: Decimal) -> Decimal:
        if v != v.to_integral_value():
            raise ValueError("local_amount doit etre un montant entier (pas de decimales) pour Yellow Card")
        return v


class CryptoSendCreateRequest(BaseModel):
    """Paiement depuis le solde du partenaire Yellow Card vers une adresse crypto
    externe (ex-"Settlement"). Contrairement aux depots/retraits, Yellow Card ne
    demande pas de KYC destinataire ici, mais une identification du proprietaire du
    wallet (travel rule)."""

    client_reference: str = Field(..., description="Idempotency key propre au projet appelant")
    customer_uid: str | None = Field(
        None, description="Identifiant interne du client (non transmis a Yellow Card, pour notre audit)"
    )

    amount: Decimal = Field(..., gt=0, description="Montant en crypto-monnaie (decimales autorisees)")
    wallet_address: str = Field(..., description="Adresse du wallet destinataire")
    crypto_currency: str = Field(..., description="Ex: USDC, USDT")
    crypto_network: str = Field(..., description="Ex: ERC20, XLM, TRC20")

    travel_rule_name: str = Field(..., description="Nom du proprietaire du wallet destinataire")
    travel_rule_business_registration_number: str = Field(
        ..., description="Numero d'enregistrement business du proprietaire du wallet"
    )


class TransactionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    type: str
    reference: str
    client_reference: str | None
    yellowcard_reference: str | None
    status: str
    amount: Decimal
    currency_code: str
    failure_reason: str | None
    initiated_at: datetime
    completed_at: datetime | None
    created_at: datetime
    updated_at: datetime
