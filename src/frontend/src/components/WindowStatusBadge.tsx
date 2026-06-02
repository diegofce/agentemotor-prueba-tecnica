import type { WindowStatus } from "../types/policy";
import { getWindowStatusLabel } from "../utils/labels";

interface WindowStatusBadgeProps {
  windowStatus: WindowStatus | null;
}

export function WindowStatusBadge({ windowStatus }: WindowStatusBadgeProps) {
  if (windowStatus === null) {
    return <span className="badge badge-neutral">—</span>;
  }

  return (
    <span className={`badge badge-${windowStatus}`}>
      {getWindowStatusLabel(windowStatus)}
    </span>
  );
}
