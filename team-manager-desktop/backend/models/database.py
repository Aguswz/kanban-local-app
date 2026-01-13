"""
🗄️ Modelos de Base de Datos
Definición de tablas SQLAlchemy para Team Manager
"""

from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, Text, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
from typing import List, Optional
import json

Base = declarative_base()

# Tablas de asociación many-to-many
team_members = Table(
    'team_members',
    Base.metadata,
    Column('team_id', String, ForeignKey('teams.id'), primary_key=True),
    Column('user_id', String, ForeignKey('users.id'), primary_key=True),
    Column('role', String, nullable=False),
    Column('capacity', Float, default=8.0),
    Column('joined_at', DateTime, default=func.now()),
    Column('is_active', Boolean, default=True)
)

project_teams = Table(
    'project_teams',
    Base.metadata,
    Column('project_id', String, ForeignKey('projects.id'), primary_key=True),
    Column('team_id', String, ForeignKey('teams.id'), primary_key=True),
    Column('assigned_at', DateTime, default=func.now())
)

card_dependencies = Table(
    'card_dependencies',
    Base.metadata,
    Column('card_id', String, ForeignKey('cards.id'), primary_key=True),
    Column('depends_on_id', String, ForeignKey('cards.id'), primary_key=True),
    Column('created_at', DateTime, default=func.now())
)

class User(Base):
    """Modelo de Usuario"""
    __tablename__ = 'users'
    
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    avatar = Column(String)
    role = Column(String, nullable=False, default='member')  # admin, manager, member
    skills = Column(Text)  # JSON array
    capacity = Column(Float, default=8.0)  # Horas por día
    timezone = Column(String, default='UTC')
    is_active = Column(Boolean, default=True)
    
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relaciones
    teams = relationship("Team", secondary=team_members, back_populates="members")
    assigned_cards = relationship("Card", back_populates="assignee")
    availability = relationship("UserAvailability", back_populates="user")
    workload_data = relationship("WorkloadData", back_populates="user")
    
    @property
    def skills_list(self) -> List[str]:
        return json.loads(self.skills) if self.skills else []
    
    @skills_list.setter
    def skills_list(self, value: List[str]):
        self.skills = json.dumps(value)

class Team(Base):
    """Modelo de Equipo"""
    __tablename__ = 'teams'
    
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    color = Column(String, default='#3b82f6')
    
    # Configuración
    wip_limits = Column(Text)  # JSON object
    settings = Column(Text)  # JSON object
    
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relaciones
    members = relationship("User", secondary=team_members, back_populates="teams")
    projects = relationship("Project", secondary=project_teams, back_populates="teams")
    boards = relationship("Board", back_populates="team")
    cards = relationship("Card", back_populates="team")
    
    @property
    def wip_limits_dict(self) -> dict:
        return json.loads(self.wip_limits) if self.wip_limits else {}
    
    @wip_limits_dict.setter
    def wip_limits_dict(self, value: dict):
        self.wip_limits = json.dumps(value)
    
    @property
    def settings_dict(self) -> dict:
        return json.loads(self.settings) if self.settings else {}
    
    @settings_dict.setter
    def settings_dict(self, value: dict):
        self.settings = json.dumps(value)

class Project(Base):
    """Modelo de Proyecto"""
    __tablename__ = 'projects'
    
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    status = Column(String, nullable=False, default='planning')  # planning, active, on_hold, completed, cancelled
    priority = Column(String, nullable=False, default='medium')  # critical, high, medium, low
    
    # Fechas
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    
    # Estimaciones
    estimated_hours = Column(Float)
    actual_hours = Column(Float, default=0.0)
    progress = Column(Float, default=0.0)  # 0-100
    
    # Metadatos
    tags = Column(Text)  # JSON array
    dependencies = Column(Text)  # JSON array de project IDs
    
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relaciones
    teams = relationship("Team", secondary=project_teams, back_populates="projects")
    boards = relationship("Board", back_populates="project")
    cards = relationship("Card", back_populates="project")
    
    @property
    def tags_list(self) -> List[str]:
        return json.loads(self.tags) if self.tags else []
    
    @tags_list.setter
    def tags_list(self, value: List[str]):
        self.tags = json.dumps(value)
    
    @property
    def dependencies_list(self) -> List[str]:
        return json.loads(self.dependencies) if self.dependencies else []
    
    @dependencies_list.setter
    def dependencies_list(self, value: List[str]):
        self.dependencies = json.dumps(value)

class Board(Base):
    """Modelo de Tablero Kanban"""
    __tablename__ = 'boards'
    
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    team_id = Column(String, ForeignKey('teams.id'), nullable=False)
    project_id = Column(String, ForeignKey('projects.id'))
    
    # Configuración
    wip_limits = Column(Text)  # JSON object
    settings = Column(Text)  # JSON object
    
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relaciones
    team = relationship("Team", back_populates="boards")
    project = relationship("Project", back_populates="boards")
    columns = relationship("Column", back_populates="board", order_by="Column.position")

class Column(Base):
    """Modelo de Columna de Tablero"""
    __tablename__ = 'columns'
    
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    board_id = Column(String, ForeignKey('boards.id'), nullable=False)
    column_type = Column(String, nullable=False)  # backlog, ready, in_progress, review, blocked, done
    position = Column(Integer, nullable=False)
    wip_limit = Column(Integer)
    
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relaciones
    board = relationship("Board", back_populates="columns")
    cards = relationship("Card", back_populates="column", order_by="Card.position")

class Card(Base):
    """Modelo de Tarjeta"""
    __tablename__ = 'cards'
    
    id = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    
    # Clasificación
    card_type = Column(String, nullable=False, default='task')  # epic, story, task, bug, improvement
    priority = Column(String, nullable=False, default='medium')  # critical, high, medium, low
    status = Column(String, nullable=False, default='backlog')  # backlog, ready, in_progress, review, blocked, done
    
    # Asignación
    team_id = Column(String, ForeignKey('teams.id'), nullable=False)
    project_id = Column(String, ForeignKey('projects.id'), nullable=False)
    column_id = Column(String, ForeignKey('columns.id'), nullable=False)
    assigned_to = Column(String, ForeignKey('users.id'))
    position = Column(Integer, default=0)
    
    # Estimaciones y tiempo
    estimated_hours = Column(Float)
    actual_hours = Column(Float, default=0.0)
    story_points = Column(Integer)
    
    # Estado
    blocked_reason = Column(Text)
    
    # Metadatos
    tags = Column(Text)  # JSON array
    acceptance_criteria = Column(Text)  # JSON array
    
    # Fechas
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    started_at = Column(DateTime)
    completed_at = Column(DateTime)
    
    # Relaciones
    team = relationship("Team", back_populates="cards")
    project = relationship("Project", back_populates="cards")
    column = relationship("Column", back_populates="cards")
    assignee = relationship("User", back_populates="assigned_cards")
    comments = relationship("Comment", back_populates="card")
    time_entries = relationship("TimeEntry", back_populates="card")
    
    # Dependencies (many-to-many self-referential)
    dependencies = relationship(
        "Card",
        secondary=card_dependencies,
        primaryjoin=id == card_dependencies.c.card_id,
        secondaryjoin=id == card_dependencies.c.depends_on_id,
        back_populates="dependents"
    )
    dependents = relationship(
        "Card",
        secondary=card_dependencies,
        primaryjoin=id == card_dependencies.c.depends_on_id,
        secondaryjoin=id == card_dependencies.c.card_id,
        back_populates="dependencies"
    )
    
    @property
    def tags_list(self) -> List[str]:
        return json.loads(self.tags) if self.tags else []
    
    @tags_list.setter
    def tags_list(self, value: List[str]):
        self.tags = json.dumps(value)
    
    @property
    def acceptance_criteria_list(self) -> List[str]:
        return json.loads(self.acceptance_criteria) if self.acceptance_criteria else []
    
    @acceptance_criteria_list.setter
    def acceptance_criteria_list(self, value: List[str]):
        self.acceptance_criteria = json.dumps(value)

class Comment(Base):
    """Modelo de Comentario"""
    __tablename__ = 'comments'
    
    id = Column(String, primary_key=True)
    content = Column(Text, nullable=False)
    card_id = Column(String, ForeignKey('cards.id'), nullable=False)
    author_id = Column(String, ForeignKey('users.id'), nullable=False)
    
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relaciones
    card = relationship("Card", back_populates="comments")
    author = relationship("User")

class TimeEntry(Base):
    """Modelo de Registro de Tiempo"""
    __tablename__ = 'time_entries'
    
    id = Column(String, primary_key=True)
    card_id = Column(String, ForeignKey('cards.id'), nullable=False)
    user_id = Column(String, ForeignKey('users.id'), nullable=False)
    
    hours = Column(Float, nullable=False)
    description = Column(Text)
    date = Column(DateTime, nullable=False)
    
    created_at = Column(DateTime, default=func.now())
    
    # Relaciones
    card = relationship("Card", back_populates="time_entries")
    user = relationship("User")

class UserAvailability(Base):
    """Modelo de Disponibilidad de Usuario"""
    __tablename__ = 'user_availability'
    
    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey('users.id'), nullable=False)
    date = Column(DateTime, nullable=False)
    hours = Column(Float, nullable=False)
    note = Column(Text)
    
    created_at = Column(DateTime, default=func.now())
    
    # Relaciones
    user = relationship("User", back_populates="availability")

class WorkloadData(Base):
    """Modelo de Datos de Carga de Trabajo"""
    __tablename__ = 'workload_data'
    
    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey('users.id'), nullable=False)
    team_id = Column(String, ForeignKey('teams.id'), nullable=False)
    date = Column(DateTime, nullable=False)
    
    planned_hours = Column(Float, default=0.0)
    actual_hours = Column(Float, default=0.0)
    capacity = Column(Float, nullable=False)
    utilization = Column(Float, default=0.0)  # 0-1
    overloaded = Column(Boolean, default=False)
    
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relaciones
    user = relationship("User", back_populates="workload_data")
    team = relationship("Team")

class Risk(Base):
    """Modelo de Riesgo"""
    __tablename__ = 'risks'
    
    id = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    severity = Column(String, nullable=False)  # low, medium, high, critical
    probability = Column(Float, nullable=False)  # 0-1
    impact = Column(Float, nullable=False)  # 0-1
    category = Column(String, nullable=False)  # technical, resource, timeline, quality, external
    
    # Entidades afectadas
    affected_teams = Column(Text)  # JSON array
    affected_projects = Column(Text)  # JSON array
    
    # Gestión
    mitigation = Column(Text)
    owner_id = Column(String, ForeignKey('users.id'))
    status = Column(String, default='open')  # open, mitigating, resolved
    
    detected_at = Column(DateTime, default=func.now())
    resolved_at = Column(DateTime)
    
    # Relaciones
    owner = relationship("User")
    
    @property
    def affected_teams_list(self) -> List[str]:
        return json.loads(self.affected_teams) if self.affected_teams else []
    
    @affected_teams_list.setter
    def affected_teams_list(self, value: List[str]):
        self.affected_teams = json.dumps(value)
    
    @property
    def affected_projects_list(self) -> List[str]:
        return json.loads(self.affected_projects) if self.affected_projects else []
    
    @affected_projects_list.setter
    def affected_projects_list(self, value: List[str]):
        self.affected_projects = json.dumps(value)

class AIInsight(Base):
    """Modelo de Insight de IA"""
    __tablename__ = 'ai_insights'
    
    id = Column(String, primary_key=True)
    insight_type = Column(String, nullable=False)  # bottleneck, overload, underutilization, dependency, quality, timeline
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    severity = Column(String, nullable=False)  # info, warning, critical
    confidence = Column(Float, nullable=False)  # 0-1
    
    # Recomendaciones
    recommendations = Column(Text)  # JSON array
    
    # Entidades afectadas
    affected_teams = Column(Text)  # JSON array
    affected_projects = Column(Text)  # JSON array
    affected_users = Column(Text)  # JSON array
    
    acknowledged = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now())
    
    @property
    def recommendations_list(self) -> List[str]:
        return json.loads(self.recommendations) if self.recommendations else []
    
    @recommendations_list.setter
    def recommendations_list(self, value: List[str]):
        self.recommendations = json.dumps(value)
    
    @property
    def affected_teams_list(self) -> List[str]:
        return json.loads(self.affected_teams) if self.affected_teams else []
    
    @affected_teams_list.setter
    def affected_teams_list(self, value: List[str]):
        self.affected_teams = json.dumps(value)
    
    @property
    def affected_projects_list(self) -> List[str]:
        return json.loads(self.affected_projects) if self.affected_projects else []
    
    @affected_projects_list.setter
    def affected_projects_list(self, value: List[str]):
        self.affected_projects = json.dumps(value)
    
    @property
    def affected_users_list(self) -> List[str]:
        return json.loads(self.affected_users) if self.affected_users else []
    
    @affected_users_list.setter
    def affected_users_list(self, value: List[str]):
        self.affected_users = json.dumps(value)