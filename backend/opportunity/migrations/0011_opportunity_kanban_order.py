# Generated manually for Opportunity Kanban feature.

from django.db import migrations, models


def assign_kanban_order(apps, schema_editor):
    """Seed kanban_order for existing rows: group by (org, stage), order by
    -created_at, stride 1000 so future drag-drop can average neighbors."""
    Opportunity = apps.get_model("opportunity", "Opportunity")
    combinations = Opportunity.objects.values("org_id", "stage").distinct()
    for combo in combinations:
        opps = Opportunity.objects.filter(
            org_id=combo["org_id"], stage=combo["stage"]
        ).order_by("-created_at")
        for index, opp in enumerate(opps):
            opp.kanban_order = (index + 1) * 1000
            opp.save(update_fields=["kanban_order"])


def reverse_kanban_order(apps, schema_editor):
    Opportunity = apps.get_model("opportunity", "Opportunity")
    Opportunity.objects.all().update(kanban_order=0)


class Migration(migrations.Migration):
    # Disable atomic mode to avoid "pending trigger events" errors from RLS
    # policies (matches tasks.0009_task_kanban).
    atomic = False

    dependencies = [
        ("opportunity", "0010_opportunity_custom_fields"),
    ]

    operations = [
        migrations.AddField(
            model_name="opportunity",
            name="kanban_order",
            field=models.DecimalField(
                decimal_places=6,
                default=0,
                help_text="Order within the kanban column for drag-drop positioning",
                max_digits=15,
                verbose_name="Kanban Order",
            ),
        ),
        migrations.AddIndex(
            model_name="opportunity",
            index=models.Index(
                fields=["stage", "kanban_order"], name="opp_stage_kanban_idx"
            ),
        ),
        migrations.RunPython(assign_kanban_order, reverse_kanban_order),
    ]
