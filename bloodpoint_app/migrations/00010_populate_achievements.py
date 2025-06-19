# Generated manually to populate achievement definitions

from django.db import migrations


def create_achievements(apps, schema_editor):
    AchievementDefinition = apps.get_model('bloodpoint_app', 'AchievementDefinition')
    
    achievements = [
        # Basic Achievements
        {
            'key': 'basic_welcome',
            'name': 'Bienvenido al Ciclo',
            'description': 'Te registraste en la aplicación.',
            'category': 'basic',
            'symbol': 'fa-user-plus',
            'required_value': 1
        },
        {
            'key': 'basic_intencion_vital',
            'name': 'Intención Vital',
            'description': 'Programaste tu primera intención de donación.',
            'category': 'basic',
            'symbol': 'fa-heart-pulse',
            'required_value': 1
        },
        {
            'key': 'basic_explorador_solidario',
            'name': 'Explorador Solidario',
            'description': 'Donaste en dos centros distintos.',
            'category': 'basic',
            'symbol': 'fa-compass',
            'required_value': 2
        },
        {
            'key': 'basic_mi_historia',
            'name': 'Mi Historia de Vida',
            'description': 'Consultaste tu historial de donaciones 5 veces.',
            'category': 'basic',
            'symbol': 'fa-history',
            'required_value': 5
        },
        
        # Level Achievements
        {
            'key': 'level_1_plaqueta',
            'name': 'Nivel 1: Plaqueta',
            'description': 'El inicio, pequeño pero esencial.',
            'category': 'level',
            'symbol': 'fa-medal',
            'required_value': 0
        },
        {
            'key': 'level_2_globulo_rojo',
            'name': 'Nivel 2: Glóbulo Rojo',
            'description': 'Energía, aporte vital.',
            'category': 'level',
            'symbol': 'fa-droplet',
            'required_value': 3
        },
        {
            'key': 'level_3_globulo_blanco',
            'name': 'Nivel 3: Glóbulo Blanco',
            'description': 'Protección, apoyo a otros.',
            'category': 'level',
            'symbol': 'fa-shield-virus',
            'required_value': 4
        },
        {
            'key': 'level_4_linfocito_t',
            'name': 'Nivel 4: Linfocito T',
            'description': 'Constancia e impacto sostenido.',
            'category': 'level',
            'symbol': 'fa-brain',
            'required_value': 7
        },
        {
            'key': 'level_5_medula_osea',
            'name': 'Nivel 5: Médula Ósea',
            'description': 'Fuente de vida.',
            'category': 'level',
            'symbol': 'fa-dna',
            'required_value': 10
        },
        {
            'key': 'level_6_corazon',
            'name': 'Nivel 6: Corazón',
            'description': 'Donante ejemplar, motor de la comunidad.',
            'category': 'level',
            'symbol': 'fa-heart',
            'required_value': 15
        },
        
        # Social Achievements
        {
            'key': 'social_embajador_flujo_lvl1',
            'name': 'Embajador del Flujo (Nivel 1)',
            'description': 'Compartiste la app en redes sociales 1 vez.',
            'category': 'social',
            'symbol': 'fa-share-nodes',
            'required_value': 1
        },
        {
            'key': 'social_embajador_flujo_lvl2',
            'name': 'Embajador del Flujo (Nivel 2)',
            'description': 'Compartiste la app 3 veces.',
            'category': 'social',
            'symbol': 'fa-share-nodes',
            'required_value': 3
        },
        {
            'key': 'social_embajador_flujo_lvl3',
            'name': 'Embajador del Flujo (Nivel 3)',
            'description': 'Compartiste la app 10 veces.',
            'category': 'social',
            'symbol': 'fa-share-nodes',
            'required_value': 10
        },
        {
            'key': 'social_vocero_vital',
            'name': 'Vocero Vital',
            'description': 'Compartiste la app 10 veces o generaste alto tráfico.',
            'category': 'social',
            'symbol': 'fa-bullhorn',
            'required_value': 10
        },
        
        # Rare Achievements
        {
            'key': 'rare_tipo_unico',
            'name': 'Tipo Único',
            'description': 'Tienes un grupo sanguíneo poco común (AB-).',
            'category': 'rare',
            'symbol': 'fa-gem',
            'required_value': 1
        },
        {
            'key': 'rare_heroe_emergencia',
            'name': 'Héroe de Emergencia',
            'description': 'Donaste en una campaña urgente.',
            'category': 'rare',
            'symbol': 'fa-shield',
            'required_value': 1
        },
        {
            'key': 'rare_donante_universal',
            'name': 'Donante Universal',
            'description': 'Logro exclusivo para donantes con grupo 0-.',
            'category': 'rare',
            'symbol': 'fa-earth-americas',
            'required_value': 1
        },
        {
            'key': 'rare_heroe_silencioso',
            'name': 'Héroe Silencioso',
            'description': 'Donaste sin compartir y sin reclamar recompensa.',
            'category': 'rare',
            'symbol': 'fa-user-secret',
            'required_value': 1
        }
    ]
    
    for achievement_data in achievements:
        AchievementDefinition.objects.get_or_create(
            key=achievement_data['key'],
            defaults=achievement_data
        )


def reverse_achievements(apps, schema_editor):
    AchievementDefinition = apps.get_model('bloodpoint_app', 'AchievementDefinition')
    AchievementDefinition.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('bloodpoint_app', '0009_achievementdefinition_campana_es_emergencia_and_more'),
    ]

    operations = [
        migrations.RunPython(create_achievements, reverse_achievements),
    ]
