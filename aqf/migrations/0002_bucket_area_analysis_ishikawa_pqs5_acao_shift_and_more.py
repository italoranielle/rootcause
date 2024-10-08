# Generated by Django 5.0.7 on 2024-08-27 23:39

import datetime
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0001_initial"),
        ("aqf", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Bucket",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=20)),
                ("is_done", models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name="Area",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("description", models.CharField(max_length=150)),
                (
                    "team",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="accounts.team"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Analysis",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("problem_description", models.CharField(max_length=250)),
                ("do_w5h2", models.BooleanField(default=True)),
                ("do_ishikawa", models.BooleanField(default=True)),
                ("do_whays", models.BooleanField(default=True)),
                ("do_action_plan", models.BooleanField(default=True)),
                (
                    "created_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.RESTRICT,
                        related_name="creator_analysis_set",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "members",
                    models.ManyToManyField(
                        related_name="member_analysis_set", to=settings.AUTH_USER_MODEL
                    ),
                ),
                (
                    "team",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.RESTRICT, to="accounts.team"
                    ),
                ),
                (
                    "area",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.RESTRICT, to="aqf.area"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Ishikawa",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "categoria",
                    models.CharField(
                        choices=[
                            ("metodo", "METODO"),
                            ("materiais", "MATERIAIS"),
                            ("mao_de_obra", "MÃO-DE-OBRA"),
                            ("maquina", "MAQUINA"),
                            ("meio_amb", "MEIO AMBIENTE"),
                            ("medicao", "MEDIÇÃO"),
                        ],
                        max_length=50,
                    ),
                ),
                (
                    "procedencia",
                    models.BigIntegerField(
                        choices=[(1, "NÃO PROCEDE"), (2, "EM ANÁLISE"), (3, "PROCEDE")],
                        default=2,
                    ),
                ),
                ("descricao", models.CharField(max_length=250)),
                (
                    "analysis",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="aqf.analysis"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Pqs5",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("pq1", models.CharField(blank=True, max_length=250, null=True)),
                ("pq2", models.CharField(blank=True, max_length=250, null=True)),
                ("pq3", models.CharField(blank=True, max_length=250, null=True)),
                ("pq4", models.CharField(blank=True, max_length=250, null=True)),
                ("pq5", models.CharField(blank=True, max_length=250, null=True)),
                (
                    "analysis",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="aqf.analysis"
                    ),
                ),
                (
                    "ishikawa",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="aqf.ishikawa",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Acao",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("titulo", models.CharField(max_length=150)),
                ("oque", models.TextField(blank=True, null=True)),
                (
                    "quando_inicio",
                    models.DateTimeField(
                        blank=True,
                        default=datetime.datetime(
                            2024,
                            8,
                            27,
                            23,
                            39,
                            50,
                            506323,
                            tzinfo=datetime.timezone.utc,
                        ),
                        null=True,
                    ),
                ),
                (
                    "quando_fim",
                    models.DateTimeField(
                        blank=True,
                        default=datetime.datetime(
                            2024,
                            8,
                            27,
                            23,
                            39,
                            50,
                            506323,
                            tzinfo=datetime.timezone.utc,
                        ),
                        null=True,
                    ),
                ),
                (
                    "quem",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "analysis",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="aqf.analysis"
                    ),
                ),
                (
                    "bucket",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.RESTRICT, to="aqf.bucket"
                    ),
                ),
                (
                    "whays",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="aqf.pqs5",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Shift",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("description", models.CharField(max_length=150)),
                (
                    "team",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.RESTRICT, to="accounts.team"
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="analysis",
            name="shift",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.RESTRICT, to="aqf.shift"
            ),
        ),
        migrations.CreateModel(
            name="W5h2",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("componente", models.CharField(max_length=250, null=True)),
                ("oque", models.TextField()),
                ("onde", models.TextField()),
                ("quando", models.TextField()),
                ("quem", models.TextField()),
                ("qual", models.TextField()),
                ("como", models.TextField()),
                ("componete_pos_intervencao", models.CharField(max_length=100)),
                ("modo_falha", models.CharField(max_length=100)),
                (
                    "status",
                    models.IntegerField(
                        choices=[
                            (1, "Criada"),
                            (2, "Preenchida"),
                            (3, "Revisada"),
                            (4, "Finalizada"),
                        ],
                        default=1,
                    ),
                ),
                (
                    "analysis",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE, to="aqf.analysis"
                    ),
                ),
                (
                    "criado_por",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.DeleteModel(
            name="Rai",
        ),
    ]
