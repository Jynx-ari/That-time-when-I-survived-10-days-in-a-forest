"""Small, separate inventory ledger for crafting materials.

The hotbar/backpack Inventory remains responsible for player-held item slots.
This ledger tracks stackable resource quantities without coupling crafting to
the UI layout.
"""

from collections.abc import Mapping


class ResourceInventory:
    def __init__(self, stack_limits: Mapping[str, int] | None = None):
        self._stack_limits = dict(stack_limits or {})
        self._amounts: dict[str, int] = {}

        for item_id, limit in self._stack_limits.items():
            if not item_id:
                raise ValueError("Item IDs cannot be empty.")
            if not isinstance(limit, int) or isinstance(limit, bool) or limit < 1:
                raise ValueError(f"Invalid stack limit for {item_id!r}.")

    @staticmethod
    def _validate_amount(amount: int) -> None:
        if not isinstance(amount, int) or isinstance(amount, bool) or amount < 1:
            raise ValueError("Amount must be a positive integer.")

    def amount(self, item_id: str) -> int:
        return self._amounts.get(item_id, 0)

    def has(self, item_id: str, amount: int = 1) -> bool:
        self._validate_amount(amount)
        return self.amount(item_id) >= amount

    def add(self, item_id: str, amount: int = 1) -> None:
        if not item_id:
            raise ValueError("Item ID cannot be empty.")
        self._validate_amount(amount)

        current = self.amount(item_id)
        new_amount = current + amount
        limit = self._stack_limits.get(item_id)

        if limit is not None and new_amount > limit:
            raise ValueError(
                f"{item_id!r} stack limit is {limit}; "
                f"adding {amount} would exceed it."
            )

        self._amounts[item_id] = new_amount

    def can_consume(self, item_id: str, amount: int = 1) -> bool:
        return self.has(item_id, amount)

    def consume(self, item_id: str, amount: int = 1) -> bool:
        return self.consume_many({item_id: amount})

    def can_consume_many(self, requirements: Mapping[str, int]) -> bool:
        if not requirements:
            return True

        for item_id, amount in requirements.items():
            if not item_id:
                raise ValueError("Item ID cannot be empty.")
            self._validate_amount(amount)
            if self.amount(item_id) < amount:
                return False

        return True

    def consume_many(self, requirements: Mapping[str, int]) -> bool:
        """Consume all requirements, or consume nothing if any are missing."""
        if not self.can_consume_many(requirements):
            return False

        for item_id, amount in requirements.items():
            remaining = self.amount(item_id) - amount
            if remaining:
                self._amounts[item_id] = remaining
            else:
                self._amounts.pop(item_id, None)

        return True

    def snapshot(self) -> dict[str, int]:
        """Return a copy so callers cannot mutate the internal ledger."""
        return dict(self._amounts)
