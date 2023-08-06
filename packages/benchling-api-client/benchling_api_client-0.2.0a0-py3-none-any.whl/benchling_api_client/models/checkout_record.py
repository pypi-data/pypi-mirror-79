from typing import Any, Dict, Optional, Union

import attr

from ..models.status import Status
from ..models.team_summary import TeamSummary
from ..models.user_summary import UserSummary


@attr.s(auto_attribs=True)
class CheckoutRecord:
    """  """

    status: Status
    assignee: Optional[Union[UserSummary, TeamSummary]]
    comment: str
    modified_at: str

    def to_dict(self) -> Dict[str, Any]:
        status = self.status.value

        if isinstance(self.assignee, UserSummary):
            assignee = self.assignee.to_dict()

        else:
            assignee = self.assignee.to_dict()

        comment = self.comment
        modified_at = self.modified_at

        return {
            "status": status,
            "assignee": assignee,
            "comment": comment,
            "modifiedAt": modified_at,
        }

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "CheckoutRecord":
        status = Status(d["status"])

        def _parse_assignee(data: Dict[str, Any]) -> Optional[Union[UserSummary, TeamSummary]]:
            assignee: Optional[Union[UserSummary, TeamSummary]]
            try:
                assignee = UserSummary.from_dict(d["assignee"])

                return assignee
            except:
                pass
            assignee = TeamSummary.from_dict(d["assignee"])

            return assignee

        assignee = _parse_assignee(d["assignee"])

        comment = d["comment"]

        modified_at = d["modifiedAt"]

        return CheckoutRecord(
            status=status,
            assignee=assignee,
            comment=comment,
            modified_at=modified_at,
        )
