from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import Rule
from app.db.session import AsyncSessionLocal
from app.schemas.rules import RuleCreate, RuleOut, RulePatch

router = APIRouter(prefix="/rules", tags=["rules"])


async def get_session():
    async with AsyncSessionLocal() as session:
        yield session


@router.get("", response_model=list[RuleOut])
async def list_rules(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Rule).order_by(Rule.id))
    return result.scalars().all()


@router.post("", response_model=RuleOut)
async def create_rule(payload: RuleCreate, session: AsyncSession = Depends(get_session)):
    rule = Rule(**payload.model_dump())
    session.add(rule)
    await session.commit()
    await session.refresh(rule)
    return rule


@router.patch("/{rule_id}", response_model=RuleOut)
async def patch_rule(rule_id: int, payload: RulePatch, session: AsyncSession = Depends(get_session)):
    rule = await session.get(Rule, rule_id)
    if not rule:
        raise HTTPException(status_code=404, detail="Rule not found")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(rule, key, value)
    await session.commit()
    await session.refresh(rule)
    return rule
