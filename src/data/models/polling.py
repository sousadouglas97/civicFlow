from sqlalchemy.orm import relationship
from config.database import Base
from sqlalchemy import (
    Integer,
    Column,
    String, 
    Text,
    Boolean,
    ForeignKey
)


class MonitoredProcesses(Base):
    __tablename__ = "monitored"
    
    process_id = Column(String, primary_key=True)
    last_movement_hash = Column(String)        #Hash do último conteúdo (SHA-256)
    check_frequency = Column(Integer)                   #Em segundos (ex: 21600 = 6h)
    is_active = Column(Boolean)                      #Se ainda deve ser monitorado
    #last_checked = DATETIME,                 #Última verificação
    
    
    

class ProcessUsers(Base):
    __tablename__ = "process_users"
    
    user_id = Column(Integer, primary_key=True)
    process_id = Column(String)
    contact_info = Column(String)
    
    monitored_id = Column(String, ForeignKey('monitored.process_id', name='fk_monitored'))
    monitored = relationship('MonitoredProcesses', name='fk_monitored')
    
    


class ProcessMovements(Base):
    __tablename__ = "process_movements"
    
    movement_id = Column(Integer, primary_key=True, autoincrement=True)
    process_id = Column(String)
    #movement_date DATETIME,
    content_hash = Column(String)
    summary = Column(Text)
    
    monitored_id = Column(String, ForeignKey('monitored.process_id', name='fk_monitored'))
    monitored = relationship('MonitoredProcesses', name='fk_monitored')
    
    
    
    