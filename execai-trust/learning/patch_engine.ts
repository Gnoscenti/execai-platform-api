type PatchProposal = {
  id: string;
  type: 'policy_rule' | 'feature_weight' | 'threshold_adjustment';
  description: string;
  confidence: number;
};

export function inferRootCauses(traceResult: any): string[] {
  return traceResult.rootCauseHypotheses || [];
}

export function proposePatches(hypotheses: string[]): PatchProposal[] {
  const proposals: PatchProposal[] = [];

  if (hypotheses.includes('missing_duplicate_check')) {
    proposals.push({
      id: 'patch_dup_check',
      type: 'policy_rule',
      description: 'Add duplicate invoice detection within 30 days',
      confidence: 0.92
    });
  }

  if (hypotheses.includes('vendor_history_not_weighted_for_recent_payment_overlap')) {
    proposals.push({
      id: 'patch_vendor_weight',
      type: 'feature_weight',
      description: 'Increase weight for recent payment overlap feature',
      confidence: 0.88
    });
  }

  return proposals;
}

export function scoreProposals(proposals: PatchProposal[]): PatchProposal[] {
  return proposals.map(p => ({ ...p, confidence: Math.min(1, p.confidence + 0.02) }));
}

export async function learnFromFlag(attestationId: string, traceFn: Function) {
  const traceResult = traceFn(attestationId);
  const hypotheses = inferRootCauses(traceResult);

  const proposals = proposePatches(hypotheses);
  const scored = scoreProposals(proposals);

  return scored.filter(p => p.confidence > 0.8);
}
