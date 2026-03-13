"""
Tests for workflow graph generation — build_saas, qa_pipeline, deploy_pipeline.
"""

from murphyx.workflows.build_saas import create_build_saas_tasks
from murphyx.workflows.qa_pipeline import create_qa_tasks
from murphyx.workflows.deploy_pipeline import create_deploy_tasks


def test_build_saas_produces_7_tasks():
    tasks = create_build_saas_tasks("Pet grooming SaaS")
    assert len(tasks) == 7
    types = {t.type for t in tasks}
    assert "plan" in types
    assert "implement_fe" in types
    assert "implement_be" in types
    assert "test_qa" in types
    assert "deploy" in types
    assert "write_docs" in types


def test_build_saas_has_workflow_id():
    tasks = create_build_saas_tasks("test")
    wids = {t.workflow_id for t in tasks}
    assert len(wids) == 1
    assert wids.pop() != ""


def test_build_saas_ordering():
    tasks = create_build_saas_tasks("test")
    ids = [t.id for t in tasks]
    assert ids.index("saas-pm") < ids.index("saas-ux")
    assert ids.index("saas-ux") < ids.index("saas-fe")
    assert ids.index("saas-fe") < ids.index("saas-qa")
    assert ids.index("saas-qa") < ids.index("saas-deploy")


def test_qa_pipeline_creates_tasks_per_ref():
    refs = ["abc/output.txt", "def/output.txt"]
    tasks = create_qa_tasks(refs)
    assert len(tasks) == 2
    assert all(t.type == "test_qa" for t in tasks)


def test_deploy_pipeline_produces_build_and_health():
    tasks = create_deploy_tasks(["ref/output.txt"])
    assert len(tasks) == 2
    assert tasks[0].id == "deploy-build"
    assert tasks[1].id == "deploy-health"
