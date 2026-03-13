"""
Tests for agent role binding and prompt loading.
"""

from murphyx.runtime.role_switcher import bind_role, unbind_role, RoleContext


def test_bind_known_role():
    ctx = bind_role("somsak_be")
    assert isinstance(ctx, RoleContext)
    assert ctx.role_id == "somsak_be"
    assert "read_file" in ctx.tools
    assert len(ctx.system_prompt) > 10


def test_bind_unknown_role_returns_fallback_prompt():
    ctx = bind_role("nonexistent_role")
    assert ctx.role_id == "nonexistent_role"
    assert "nonexistent_role" in ctx.system_prompt
    assert ctx.tools == []


def test_unbind_does_not_raise():
    unbind_role()


def test_bind_ceo_loads_prompt():
    ctx = bind_role("ceo")
    assert "Jarvis" in ctx.system_prompt or "CEO" in ctx.system_prompt
