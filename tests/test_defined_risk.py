import pytest
from market_wrap.defined_risk import bounds, intrinsic, legs, pnl, validate_structure, profile


def model(family,kind):
    return dict(family=family,kind=kind,strikes=[95,100,110,115] if family=='iron_condor' else [100,105],quantity=1,multiplier=100)


@pytest.mark.parametrize('family',['call_vertical','put_vertical','iron_condor'])
@pytest.mark.parametrize('kind',['debit','credit'])
def test_six_defined_risk_variants(family,kind):
    p=model(family,kind);validate_structure(p)
    assert bounds(p,2,7)==((-207,293) if kind=='debit' else (-307,193))
    assert sum(sign for _,_,sign in legs(p))==0
    for x in [0,95,100,105,110,115,100000]:
        assert bounds(p,2,7)[0]<=pnl(p,x,2,7)<=bounds(p,2,7)[1]
    reverse=model(family,'credit' if kind=='debit' else 'debit')
    assert intrinsic(reverse,107)==-intrinsic(p,107)
    assert 'UNKNOWN' in profile(p)


def test_condor_conventions_and_fee_inclusive_cap():
    short=model('iron_condor','credit');long=model('iron_condor','debit')
    assert intrinsic(short,105)==0 and intrinsic(short,90)==-5
    assert intrinsic(long,105)==0 and intrinsic(long,90)==5
    assert bounds(short,.05,5)[0]==-500
    assert bounds(short,.05,5.01)[0]<-500
    assert bounds(long,4.95,5)[0]==-500
    assert bounds(long,4.95,5.01)[0]<-500
    short['quantity']=2
    assert bounds(short,2,7)==(-607,393)


def test_rejects_unpaired_or_unequal_wing_models():
    for patch in [dict(family='naked_call'),dict(strikes=[100]),dict(multiplier=10),dict(quantity=1.5),dict(strikes=[95,100,110,116])]:
        p=model('iron_condor','credit');p.update(patch)
        with pytest.raises(ValueError):validate_structure(p)
