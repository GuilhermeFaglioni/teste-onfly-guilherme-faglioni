# Contrato do relatório (`report.json`) — PRESERVAÇÃO OBRIGATÓRIA

Fonte: `README.md` › "Contrato do CLI". **Nenhum agente pode alterar nomes, tipos, ordem semântica ou formato destes campos.**
Qualquer necessidade de mudança = `STATUS: ESCALATE`. Verificado automaticamente por `tests/test_schema_contract.py` (CI).

```json
{
  "report_version": "1.0",
  "generated_at": "2025-07-01T10:00:00-03:00",
  "summary": {
    "total_reservations": 0, "confirmed_reservations": 0, "cancelled_reservations": 0,
    "no_show_reservations": 0, "total_room_nights": 0,
    "total_amount_brl": "0.00", "average_nightly_rate_brl": "0.00"
  },
  "by_month": [{"month": "2025-01", "reservations": 0, "room_nights": 0, "total_brl": "0.00"}],
  "top_hotels": [{"hotel_id": "H01", "hotel_name": "Hotel Exemplo", "room_nights": 0, "total_brl": "0.00"}]
}
```

| Campo | Tipo | Regra |
|-|-|-|
| `report_version` | string | sempre `"1.0"` |
| `generated_at` | string ISO-8601 | offset fixo `-03:00`; ignorado em comparações |
| `summary.*_reservations`, `total_room_nights` | int | contagens; noites só de CONFIRMED |
| `summary.total_amount_brl`, `average_nightly_rate_brl` | string money | só CONFIRMED; média = total/noites, sem noites `"0.00"` |
| `by_month[].month` | string `YYYY-MM` | mês do check-in; ordem asc |
| `by_month[].reservations`, `room_nights` | int | só CONFIRMED |
| `top_hotels[]` | objetos | `total_brl` desc, empate `hotel_id` asc; até `--top` itens |

**Money:** string `^-?\d+\.\d{2}$`, sem separador de milhar, `Decimal` + `ROUND_HALF_UP` só na serialização.
**Chaves:** exatamente as listadas — nem a mais, nem a menos.
**CLI:** `--input` (obrig.), `--rates` (obrig.), `--output` (padrão `output/report.json`), `--top` (padrão 5, int ≥ 1).
Exit codes: `0` sucesso, `2` entrada/argumento inválido, `1` erro inesperado.
