# mode: fun
from pyalamode import Map, record, oneof, case, value_encode, value_decode

@oneof
class InvoiceStatus:
    @case
    class Ready:
        pass
    @case
    class Rejected:
        reason: str

@record
class Invoice:
    order_id: str
    total_cents: int
    labels: Map[str, str]
    status: InvoiceStatus

def quote(quantity: int, price: int = 30) -> int:
    return quantity * price

def encode_invoice(invoice: Invoice) -> bytes:
    return value_encode(invoice, Invoice)

def decode_invoice(data: bytes) -> Invoice:
    return value_decode(data, Invoice)
