"""Final read-only scientific replay with the adjudicated WTSAF2YR representation check.

This wrapper does not train, retune, or recalibrate any model. It reuses the locked
`verify_science.py` calculations and changes only the WTSAF2YR representation check:
zero-versus-positive eligibility must agree exactly, while the stored decimal weight may
differ by at most 5.0001e-5, the documented archived-vs-CDC serialization increment.
All other numeric tolerances remain unchanged.
"""
import numpy as np
import verify_science as base

WTSAF2YR_REPRESENTATION_TOL = 5.0001e-5
WTSAF2YR_JUST = (
    "WTSAF2YR eligibility is checked exactly as zero versus positive. The archived CSV "
    "stores the CDC-published maximum 944153.24975 as 944153.2498; therefore a "
    "5e-5 decimal-representation difference is permitted only for the weight value."
)


def adjudicated_cohort_match(self, label, left, right, cols):
    self.exact(label + ': identifier symmetric difference', 0, len(set(left.SEQN) ^ set(right.SEQN)))
    left = left.sort_values('SEQN').reset_index(drop=True)
    right = right.sort_values('SEQN').reset_index(drop=True)
    for c in cols:
        self.exact(label + ': ' + c + ' missingness mismatch', 0, int((left[c].isna() != right[c].isna()).sum()))
        valid = left[c].notna()
        lv = left.loc[valid, c].to_numpy()
        rv = right.loc[valid, c].to_numpy()
        gap = float(np.max(abs(lv - rv))) if len(lv) else 0.0
        if c == 'WTSAF2YR':
            self.exact(
                label + ': WTSAF2YR zero-versus-positive membership mismatch',
                0,
                int(((lv > 0) != (rv > 0)).sum()),
            )
            self.compare(
                label + ': WTSAF2YR representation max difference',
                0,
                gap,
                WTSAF2YR_REPRESENTATION_TOL,
                WTSAF2YR_JUST,
            )
        else:
            self.compare(label + ': ' + c + ' max difference', 0, gap)


base.Audit.cohort_match = adjudicated_cohort_match

if __name__ == '__main__':
    base.main()
