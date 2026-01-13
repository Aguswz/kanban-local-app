"""
🧠 Director de IA - Agente Principal de Gestión
Comportamiento como director de operaciones ágil senior
"""

import json
import os
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import openai
from anthropic import Anthropic
import logging

from models.database import Team, Project, Card, User, Risk, AIInsight

logger = logging.getLogger(__name__)

class AIDirectorService:
    """
    Director de IA que actúa como un director de operaciones ágil senior.
    
    Responsabilidades:
    - Análisis global de múltiples equipos y proyectos
    - Detección temprana de riesgos y cuellos de botella
    - Optimización de flujo de trabajo
    - Redistribución inteligente de carga
    - Coordinación entre equipos
    """
    
    def __init__(self):
        self.system_prompt = self._load_system_prompt()
        self.openai_client = None
        self.anthropic_client = None
        
        self._setup_ai_clients()
    
    def _load_system_prompt(self) -> str:
        """Cargar prompt del sistema desde archivo"""
        prompt_file = os.path.join(os.path.dirname(__file__), '..', 'prompts', 'ai_director_system.txt')
        
        try:
            with open(prompt_file, 'r', encoding='utf-8') as f:
                return f.read().strip()
        except FileNotFoundError:
            logger.warning("Archivo de prompt del sistema no encontrado, usando fallback")
            return self._get_fallback_prompt()
    
    def _get_fallback_prompt(self) -> str:
        """Prompt de respaldo integrado"""
        return """Eres un Director de Operaciones Ágil senior con experiencia real en gestión de múltiples equipos y proyectos.

COMPORTAMIENTO ESPERADO:
- Actúas como un director experimentado, no como un chatbot
- Analizas el contexto completo antes de hacer recomendaciones
- Detectas riesgos antes de que se conviertan en problemas
- Propones soluciones concretas y accionables
- Priorizas el flujo de valor sobre métricas de vanidad
- Comunicas de forma directa y profesional

RESPONSABILIDADES:
1. Análisis global de equipos y proyectos
2. Detección de cuellos de botella y sobrecarga
3. Optimización de flujo de trabajo
4. Coordinación entre equipos
5. Gestión proactiva de riesgos

FORMATO DE RESPUESTA:
Siempre devuelve JSON estructurado con:
{
  "analysis": "Análisis breve del estado actual",
  "insights": [...], // Array de insights detectados
  "risks": [...], // Array de riesgos identificados
  "recommendations": [...], // Recomendaciones específicas
  "actions": [...] // Acciones sugeridas
}

REGLAS:
- Sé conciso pero completo
- Enfócate en impacto real
- Propón soluciones, no solo problemas
- Considera dependencias entre equipos
- Respeta principios ágiles sin dogmatismo"""
    
    def _setup_ai_clients(self):
        """Configurar clientes de IA"""
        # OpenAI
        openai_key = os.getenv('OPENAI_API_KEY')
        if openai_key:
            self.openai_client = openai.OpenAI(api_key=openai_key)
            logger.info("✅ Cliente OpenAI configurado")
        
        # Anthropic
        anthropic_key = os.getenv('ANTHROPIC_API_KEY')
        if anthropic_key:
            self.anthropic_client = Anthropic(api_key=anthropic_key)
            logger.info("✅ Cliente Anthropic configurado")
        
        if not self.openai_client and not self.anthropic_client:
            logger.warning("⚠️ No hay clientes de IA configurados. Usando modo simulación.")
    
    async def analyze_global_state(self, 
                                 teams: List[Team], 
                                 projects: List[Project], 
                                 cards: List[Card],
                                 users: List[User]) -> Dict[str, Any]:
        """
        Análisis global del estado de todos los equipos y proyectos
        """
        
        # Preparar contexto completo
        context = self._prepare_global_context(teams, projects, cards, users)
        
        # Prompt específico para análisis global
        prompt = f"""
        ANÁLISIS GLOBAL REQUERIDO:
        
        Analiza el estado completo de la organización y proporciona:
        1. Evaluación del estado general
        2. Identificación de cuellos de botella críticos
        3. Detección de equipos sobrecargados o subutilizados
        4. Riesgos inter-proyecto
        5. Oportunidades de optimización
        6. Recomendaciones prioritarias
        
        CONTEXTO ORGANIZACIONAL:
        {context}
        
        Proporciona un análisis como director de operaciones experimentado.
        """
        
        # Procesar con IA
        if self.openai_client:
            response = await self._process_with_openai(prompt)
        elif self.anthropic_client:
            response = await self._process_with_anthropic(prompt)
        else:
            response = self._simulate_global_analysis(teams, projects, cards, users)
        
        return self._parse_ai_response(response)
    
    async def detect_bottlenecks(self, 
                               teams: List[Team], 
                               cards: List[Card]) -> List[Dict[str, Any]]:
        """
        Detectar cuellos de botella en el flujo de trabajo
        """
        
        bottlenecks = []
        
        for team in teams:
            team_cards = [card for card in cards if card.team_id == team.id]
            
            # Análisis por columnas/estados
            status_counts = {}
            for card in team_cards:
                status_counts[card.status] = status_counts.get(card.status, 0) + 1
            
            # Detectar acumulación excesiva
            if status_counts.get('review', 0) > 5:
                bottlenecks.append({
                    'type': 'review_bottleneck',
                    'team_id': team.id,
                    'severity': 'high',
                    'description': f'Equipo {team.name} tiene {status_counts["review"]} tarjetas en revisión',
                    'recommendation': 'Aumentar capacidad de revisión o revisar criterios'
                })
            
            if status_counts.get('blocked', 0) > 2:
                bottlenecks.append({
                    'type': 'blocked_cards',
                    'team_id': team.id,
                    'severity': 'critical',
                    'description': f'Equipo {team.name} tiene {status_counts["blocked"]} tarjetas bloqueadas',
                    'recommendation': 'Resolver bloqueos inmediatamente'
                })
        
        return bottlenecks
    
    async def optimize_workload(self, 
                              teams: List[Team], 
                              users: List[User], 
                              cards: List[Card]) -> Dict[str, Any]:
        """
        Optimizar distribución de carga de trabajo
        """
        
        # Calcular carga actual por usuario
        user_workload = {}
        for user in users:
            assigned_cards = [card for card in cards if card.assigned_to == user.id and card.status in ['ready', 'in_progress', 'review']]
            total_hours = sum(card.estimated_hours or 0 for card in assigned_cards)
            user_workload[user.id] = {
                'user': user,
                'current_load': total_hours,
                'capacity': user.capacity * 5,  # Capacidad semanal
                'utilization': total_hours / (user.capacity * 5) if user.capacity > 0 else 0,
                'cards_count': len(assigned_cards)
            }
        
        # Identificar desequilibrios
        overloaded = [uid for uid, data in user_workload.items() if data['utilization'] > 0.9]
        underutilized = [uid for uid, data in user_workload.items() if data['utilization'] < 0.6]
        
        # Generar recomendaciones
        recommendations = []
        
        if overloaded:
            recommendations.append({
                'type': 'redistribute_work',
                'priority': 'high',
                'description': f'{len(overloaded)} usuarios sobrecargados detectados',
                'affected_users': overloaded,
                'action': 'Redistribuir trabajo o ajustar estimaciones'
            })
        
        if underutilized:
            recommendations.append({
                'type': 'increase_capacity',
                'priority': 'medium',
                'description': f'{len(underutilized)} usuarios subutilizados',
                'affected_users': underutilized,
                'action': 'Asignar más trabajo o reasignar a proyectos críticos'
            })
        
        return {
            'workload_analysis': user_workload,
            'overloaded_users': overloaded,
            'underutilized_users': underutilized,
            'recommendations': recommendations
        }
    
    async def coordinate_teams(self, 
                             teams: List[Team], 
                             projects: List[Project], 
                             cards: List[Card]) -> Dict[str, Any]:
        """
        Analizar coordinación entre equipos
        """
        
        coordination_issues = []
        
        # Analizar dependencias inter-equipo
        for project in projects:
            project_teams = [team for team in teams if team.id in [pt.id for pt in project.teams]]
            
            if len(project_teams) > 1:
                # Proyecto multi-equipo, analizar coordinación
                team_progress = {}
                for team in project_teams:
                    team_cards = [card for card in cards if card.team_id == team.id and card.project_id == project.id]
                    completed = len([card for card in team_cards if card.status == 'done'])
                    total = len(team_cards)
                    team_progress[team.id] = completed / total if total > 0 else 0
                
                # Detectar desequilibrios significativos
                if team_progress:
                    max_progress = max(team_progress.values())
                    min_progress = min(team_progress.values())
                    
                    if max_progress - min_progress > 0.3:  # 30% de diferencia
                        coordination_issues.append({
                            'type': 'team_sync_issue',
                            'project_id': project.id,
                            'severity': 'medium',
                            'description': f'Desincronización entre equipos en {project.name}',
                            'team_progress': team_progress,
                            'recommendation': 'Sincronizar equipos y revisar dependencias'
                        })
        
        return {
            'coordination_issues': coordination_issues,
            'multi_team_projects': len([p for p in projects if len(p.teams) > 1])
        }
    
    def _prepare_global_context(self, teams: List[Team], projects: List[Project], 
                               cards: List[Card], users: List[User]) -> str:
        """Preparar contexto global para la IA"""
        
        context = {
            'timestamp': datetime.now().isoformat(),
            'summary': {
                'teams_count': len(teams),
                'projects_count': len(projects),
                'active_projects': len([p for p in projects if p.status == 'active']),
                'users_count': len(users),
                'total_cards': len(cards),
                'cards_by_status': {}
            },
            'teams': [],
            'projects': [],
            'workload_indicators': {}
        }
        
        # Resumen de tarjetas por estado
        for card in cards:
            status = card.status
            context['summary']['cards_by_status'][status] = context['summary']['cards_by_status'].get(status, 0) + 1
        
        # Información de equipos
        for team in teams:
            team_cards = [card for card in cards if card.team_id == team.id]
            context['teams'].append({
                'id': team.id,
                'name': team.name,
                'members_count': len(team.members),
                'cards_count': len(team_cards),
                'wip_limits': team.wip_limits_dict,
                'active_cards': len([card for card in team_cards if card.status in ['ready', 'in_progress', 'review']])
            })
        
        # Información de proyectos
        for project in projects:
            project_cards = [card for card in cards if card.project_id == project.id]
            completed_cards = len([card for card in project_cards if card.status == 'done'])
            
            context['projects'].append({
                'id': project.id,
                'name': project.name,
                'status': project.status,
                'priority': project.priority,
                'teams_count': len(project.teams),
                'progress': project.progress,
                'cards_completed': completed_cards,
                'cards_total': len(project_cards)
            })
        
        return json.dumps(context, indent=2, default=str)
    
    async def _process_with_openai(self, prompt: str) -> str:
        """Procesar con OpenAI"""
        try:
            response = await self.openai_client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,
                max_tokens=3000
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error con OpenAI: {e}")
            return self._get_error_response(str(e))
    
    async def _process_with_anthropic(self, prompt: str) -> str:
        """Procesar con Anthropic"""
        try:
            response = await self.anthropic_client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=3000,
                temperature=0.1,
                system=self.system_prompt,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text
        except Exception as e:
            logger.error(f"Error con Anthropic: {e}")
            return self._get_error_response(str(e))
    
    def _simulate_global_analysis(self, teams: List[Team], projects: List[Project], 
                                cards: List[Card], users: List[User]) -> str:
        """Simulación de análisis global para desarrollo"""
        
        # Calcular métricas básicas
        active_projects = len([p for p in projects if p.status == 'active'])
        blocked_cards = len([c for c in cards if c.status == 'blocked'])
        review_cards = len([c for c in cards if c.status == 'review'])
        
        # Análisis simulado como director senior
        analysis = {
            "analysis": f"Organización con {len(teams)} equipos gestionando {active_projects} proyectos activos. {blocked_cards} bloqueos y {review_cards} elementos en revisión requieren atención.",
            "insights": [
                {
                    "type": "bottleneck" if review_cards > 10 else "flow_health",
                    "title": "Estado del flujo de revisión",
                    "description": f"Hay {review_cards} elementos en revisión. {'Posible cuello de botella' if review_cards > 10 else 'Flujo saludable'}",
                    "severity": "warning" if review_cards > 10 else "info",
                    "confidence": 0.85,
                    "recommendations": ["Aumentar capacidad de revisión", "Revisar criterios de aceptación"] if review_cards > 10 else ["Mantener ritmo actual"],
                    "affected_teams": [team.id for team in teams[:2]] if review_cards > 10 else []
                }
            ],
            "risks": [
                {
                    "title": "Bloqueos acumulados",
                    "description": f"Se detectaron {blocked_cards} tarjetas bloqueadas que pueden impactar la entrega",
                    "severity": "high" if blocked_cards > 5 else "medium",
                    "probability": 0.8 if blocked_cards > 5 else 0.4,
                    "impact": 0.7,
                    "category": "timeline",
                    "affected_teams": [team.id for team in teams if any(c.status == 'blocked' and c.team_id == team.id for c in cards)]
                }
            ] if blocked_cards > 0 else [],
            "recommendations": [
                "Resolver bloqueos prioritarios inmediatamente",
                "Establecer daily review de impedimentos",
                "Mejorar coordinación entre equipos" if len(teams) > 3 else "Mantener comunicación fluida"
            ],
            "actions": [
                {
                    "type": "UNBLOCK_CARDS",
                    "priority": "high",
                    "description": "Desbloquear tarjetas críticas",
                    "affected_cards": [c.id for c in cards if c.status == 'blocked'][:5]
                }
            ] if blocked_cards > 0 else []
        }
        
        return json.dumps(analysis, indent=2, default=str)
    
    def _get_error_response(self, error_message: str) -> str:
        """Respuesta de error estructurada"""
        return json.dumps({
            "analysis": f"Error en análisis: {error_message}",
            "insights": [],
            "risks": [{
                "title": "Error del sistema de IA",
                "description": f"El director de IA encontró un error: {error_message}",
                "severity": "medium",
                "probability": 1.0,
                "impact": 0.3,
                "category": "technical"
            }],
            "recommendations": [
                "Verificar configuración de IA",
                "Revisar conectividad",
                "Usar análisis manual temporal"
            ],
            "actions": []
        })
    
    def _parse_ai_response(self, response: str) -> Dict[str, Any]:
        """Parsear y validar respuesta de IA"""
        try:
            data = json.loads(response)
            
            # Validar estructura básica
            required_fields = ['analysis', 'insights', 'risks', 'recommendations']
            for field in required_fields:
                if field not in data:
                    data[field] = [] if field != 'analysis' else 'Análisis no disponible'
            
            return data
            
        except json.JSONDecodeError as e:
            logger.error(f"Error parseando respuesta de IA: {e}")
            return {
                "analysis": "Error parseando respuesta de IA",
                "insights": [],
                "risks": [],
                "recommendations": ["Revisar configuración del sistema de IA"],
                "actions": []
            }
    
    def get_available_providers(self) -> Dict[str, bool]:
        """Obtener proveedores de IA disponibles"""
        return {
            "openai": self.openai_client is not None,
            "anthropic": self.anthropic_client is not None,
            "simulation": True
        }