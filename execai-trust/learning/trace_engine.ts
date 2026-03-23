export type TraceNode = {
  id: string;
  type: 'input' | 'context' | 'policy' | 'score' | 'approval' | 'execution' | 'flag';
  label: string;
  metadata?: Record<string, unknown>;
};

export type TraceEdge = {
  from: string;
  to: string;
  reason: string;
};

export type TraceResult = {
  attestationId: string;
  nodes: TraceNode[];
  edges: TraceEdge[];
  rootCauseHypotheses: string[];
};

export function trace(attestationId: string): TraceResult {
  const nodes: TraceNode[] = [
    { id: 'invoice_4421', type: 'input', label: 'Invoice INV-4421' },
    { id: 'vendor_v88', type: 'context', label: 'Vendor V-88', metadata: { recentlyAdded: true } },
    { id: 'rule_amount_threshold', type: 'policy', label: 'Amount threshold check' },
    { id: 'risk_082', type: 'score', label: 'Risk score 0.82' },
    { id: 'hitl_finance_admin', type: 'approval', label: 'Approved by finance_admin_02' },
    { id: 'payment_exec', type: 'execution', label: 'Payment executed' }
  ];

  const edges: TraceEdge[] = [
    { from: 'invoice_4421', to: 'risk_082', reason: 'invoice amount and due date influenced risk' },
    { from: 'vendor_v88', to: 'risk_082', reason: 'new vendor status increased risk' },
    { from: 'rule_amount_threshold', to: 'risk_082', reason: 'threshold rule scored high-risk path' },
    { from: 'risk_082', to: 'hitl_finance_admin', reason: 'tier_1 required approval' },
    { from: 'hitl_finance_admin', to: 'payment_exec', reason: 'human approval permitted execution' }
  ];

  const rootCauseHypotheses = [
    'missing_duplicate_check',
    'vendor_history_not_weighted_for_recent_payment_overlap'
  ];

  return {
    attestationId,
    nodes,
    edges,
    rootCauseHypotheses
  };
}
