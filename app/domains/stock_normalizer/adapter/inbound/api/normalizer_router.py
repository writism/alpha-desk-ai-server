from fastapi import APIRouter, HTTPException

from app.domains.stock_normalizer.adapter.outbound.persistence.normalized_disclosure_repository_impl import InMemoryNormalizedDisclosureRepository
from app.domains.stock_normalizer.application.request.normalize_disclosure_request import NormalizeDisclosureRequest
from app.domains.stock_normalizer.application.response.normalize_disclosure_response import NormalizeDisclosureResponse
from app.domains.stock_normalizer.application.usecase.normalize_disclosure_usecase import NormalizeDisclosureUseCase

router = APIRouter(prefix="/normalizer/disclosures", tags=["stock_normalizer"])

_repository = InMemoryNormalizedDisclosureRepository()


def _get_use_case() -> NormalizeDisclosureUseCase:
    return NormalizeDisclosureUseCase(_repository)


@router.post("", response_model=NormalizeDisclosureResponse, status_code=201)
async def normalize_disclosure(request: NormalizeDisclosureRequest):
    try:
        return await _get_use_case().execute(request)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
