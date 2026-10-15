from fastapi import FastAPI, Request, Depends
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from contextlib import asynccontextmanager
from database import engine, Base
from auth.dependencies import require_auth
import models.ucc
import models.order
import models.switch
import models.xsip
import models.sip_topup
import models.sip
import models.stp
import models.swp
import models.order_cancellation
import models.sip_cancellation
import models.xsip_cancellation
import models.daily_xsip_cancellation
import models.stp_cancellation
import models.client_bank_detail
import models.mandate_registration
import models.utr_update
import models.fatca_registration
import models.fatca_common
import models.stp_modification
import models.swp_modification
import models.sip_amc_pause
from routers import ucc, order, switch, xsip, sip_topup, sip, stp, swp, order_cancellation, sip_cancellation, xsip_cancellation, daily_xsip_cancellation, stp_cancellation, client_bank_detail, mandate_registration, mandate_image_upload, utr_update, sip_umrn_mapping, order_status_report, mandate_status_report, communication, fatca_registration, fatca_common, aof_image_upload, fatca_image_upload, elog_upload, poa_upload, cancel_cheque_upload, member_fund_allocation, redemption_payout, statement_reports, misc_reports, misc_services, stp_modification, swp_modification, sip_amc_pause, auth
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(
    title="NSE Mutual Fund API",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(status_code=500, content={"detail": str(exc)})


app.include_router(auth.router, prefix="/api/v1")
app.include_router(ucc.router, prefix="/api/v1", dependencies=[Depends(require_auth)])
app.include_router(order.router, prefix="/api/v1", dependencies=[Depends(require_auth)])
app.include_router(switch.router, prefix="/api/v1", dependencies=[Depends(require_auth)])
app.include_router(xsip.router, prefix="/api/v1", dependencies=[Depends(require_auth)])
app.include_router(sip_topup.router, prefix="/api/v1", dependencies=[Depends(require_auth)])
app.include_router(sip.router, prefix="/api/v1", dependencies=[Depends(require_auth)])
app.include_router(stp.router, prefix="/api/v1", dependencies=[Depends(require_auth)])
app.include_router(swp.router, prefix="/api/v1", dependencies=[Depends(require_auth)])
app.include_router(order_cancellation.router, prefix="/api/v1", dependencies=[Depends(require_auth)])
app.include_router(sip_cancellation.router, prefix="/api/v1", dependencies=[Depends(require_auth)])
app.include_router(xsip_cancellation.router, prefix="/api/v1", dependencies=[Depends(require_auth)])
app.include_router(daily_xsip_cancellation.router, prefix="/api/v1", dependencies=[Depends(require_auth)])
app.include_router(stp_cancellation.router, prefix="/api/v1", dependencies=[Depends(require_auth)])
app.include_router(client_bank_detail.router, prefix="/api/v1", dependencies=[Depends(require_auth)])
app.include_router(mandate_registration.router, prefix="/api/v1", dependencies=[Depends(require_auth)])
app.include_router(mandate_image_upload.router, prefix="/api/v1", dependencies=[Depends(require_auth)])
app.include_router(utr_update.router, prefix="/api/v1", dependencies=[Depends(require_auth)])
app.include_router(sip_umrn_mapping.router, prefix="/api/v1", dependencies=[Depends(require_auth)])
app.include_router(order_status_report.router, prefix="/api/v1", dependencies=[Depends(require_auth)])
app.include_router(mandate_status_report.router, prefix="/api/v1", dependencies=[Depends(require_auth)])
app.include_router(communication.router, prefix="/api/v1", dependencies=[Depends(require_auth)])
app.include_router(fatca_registration.router, prefix="/api/v1", dependencies=[Depends(require_auth)])
app.include_router(fatca_common.router, prefix="/api/v1", dependencies=[Depends(require_auth)])
app.include_router(aof_image_upload.router, prefix="/api/v1", dependencies=[Depends(require_auth)])
app.include_router(fatca_image_upload.router, prefix="/api/v1", dependencies=[Depends(require_auth)])
app.include_router(elog_upload.router, prefix="/api/v1", dependencies=[Depends(require_auth)])
app.include_router(poa_upload.router, prefix="/api/v1", dependencies=[Depends(require_auth)])
app.include_router(cancel_cheque_upload.router, prefix="/api/v1", dependencies=[Depends(require_auth)])
app.include_router(member_fund_allocation.router, prefix="/api/v1", dependencies=[Depends(require_auth)])
app.include_router(redemption_payout.router, prefix="/api/v1", dependencies=[Depends(require_auth)])
app.include_router(statement_reports.router, prefix="/api/v1", dependencies=[Depends(require_auth)])
app.include_router(misc_reports.router, prefix="/api/v1", dependencies=[Depends(require_auth)])
app.include_router(misc_services.router, prefix="/api/v1", dependencies=[Depends(require_auth)])
app.include_router(stp_modification.router, prefix="/api/v1", dependencies=[Depends(require_auth)])
app.include_router(swp_modification.router, prefix="/api/v1", dependencies=[Depends(require_auth)])
app.include_router(sip_amc_pause.router, prefix="/api/v1", dependencies=[Depends(require_auth)])


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    schema = get_openapi(
        title=app.title,
        version=app.version,
        routes=app.routes,
    )
    schema.setdefault("components", {})["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "BASIC",
            "description": "Paste the access_token from POST /api/v1/auth/login",
        }
    }
    for path in schema["paths"].values():
        for method in path.values():
            method["security"] = [{"BearerAuth": []}]
    app.openapi_schema = schema
    return schema


app.openapi = custom_openapi


@app.get("/health")
async def health():
    return {"status": "ok"}
