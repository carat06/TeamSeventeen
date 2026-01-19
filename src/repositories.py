# repositories.py
from sqlalchemy import (
    create_engine, Column, Integer, String, Float, DateTime, JSON, ForeignKey
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime, timedelta

Base = declarative_base()

# -----------------------------
# Case model
# -----------------------------
class CaseModel(Base):
    __tablename__ = "cases"

    case_id = Column(Integer, primary_key=True, autoincrement=True)
    invoice_number = Column(String)
    account_number = Column(String)
    risk_score = Column(Float)
    risk_level = Column(String)
    priority_level = Column(String)
    strategy = Column(String)
    status = Column(String)
    assigned_dca = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


# -----------------------------
# Event model
# -----------------------------
class EventModel(Base):
    __tablename__ = "case_events"

    event_id = Column(Integer, primary_key=True, autoincrement=True)
    case_id = Column(Integer, ForeignKey("cases.case_id"))
    event_type = Column(String)
    from_status = Column(String)
    to_status = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
    actor = Column(String)
    case_metadata = Column(JSON)


# -----------------------------
# SLA model
# -----------------------------
class SLAInstance(Base):
    __tablename__ = "sla_instances"

    sla_id = Column(Integer, primary_key=True, autoincrement=True)
    case_id = Column(Integer, ForeignKey("cases.case_id"))
    stage = Column(String)
    deadline = Column(DateTime)
    breached = Column(String, default="False")
    breached_at = Column(DateTime, nullable=True)


# -----------------------------
# Case Repository
# -----------------------------
class CaseRepository:
    def __init__(self, db_url="postgresql://postgres:Simba%40postgresql@localhost:5432/dca_management"):
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    # Single case save
    def save_case(self, case: CaseModel):
        session = self.Session()
        try:
            session.add(case)
            session.commit()
        except Exception as e:
            session.rollback()
            print(f"⚠️ Error saving case {case.case_id}: {e}")
        finally:
            session.close()

    # Bulk save
    def save_bulk(self, cases):
        """Save multiple CaseModel objects in bulk."""
        if not cases:
            return
        session = self.Session()
        try:
            session.bulk_save_objects(cases)
            session.commit()
        except Exception as e:
            session.rollback()
            print(f"⚠️ Error saving bulk cases: {e}")
        finally:
            session.close()

    # Retrieve a single case
    def get_case(self, case_id):
        session = self.Session()
        case = session.query(CaseModel).filter_by(case_id=case_id).first()
        session.close()
        return case

    # Retrieve all cases
    def all_cases(self):
        session = self.Session()
        cases = session.query(CaseModel).all()
        session.close()
        return cases


# -----------------------------
# Event Repository
# -----------------------------
class EventRepository:
    def __init__(self, db_url="postgresql://postgres:Simba%40postgresql@localhost:5432/dca_management"):
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    # Log single event
    def log_event(
        self, case_id, event_type, from_status, to_status, actor="SYSTEM", metadata=None
    ):
        session = self.Session()
        try:
            event = EventModel(
                case_id=case_id,
                event_type=event_type,
                from_status=from_status,
                to_status=to_status,
                actor=actor,
                case_metadata=metadata or {},
            )
            session.add(event)
            session.commit()
        except Exception as e:
            session.rollback()
            print(f"⚠️ Error logging event for case {case_id}: {e}")
        finally:
            session.close()

    # Bulk log events
    def log_bulk_events(self, events):
        """Accepts a list of EventModel objects and saves them in one commit"""
        if not events:
            return
        session = self.Session()
        try:
            session.bulk_save_objects(events)
            session.commit()
        except Exception as e:
            session.rollback()
            print(f"⚠️ Error logging bulk events: {e}")
        finally:
            session.close()


# -----------------------------
# SLA Engine
# -----------------------------
class SLAEngine:
    """
    Creates SLA instance(s) for the next stage
    """
    def __init__(self, db_url="postgresql://postgres:Simba%40postgresql@localhost:5432/dca_management"):
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    # Create single SLA
    def create_sla(self, case_id, stage, hours_to_complete=24):
        session = self.Session()
        try:
            sla = SLAInstance(
                case_id=case_id,
                stage=stage,
                deadline=datetime.utcnow() + timedelta(hours=hours_to_complete),
                breached="False",
            )
            session.add(sla)
            session.commit()
        except Exception as e:
            session.rollback()
            print(f"⚠️ Error creating SLA for case {case_id}: {e}")
        finally:
            session.close()

    # Bulk SLA creation
    def create_bulk_slas(self, sla_list):
        """Accepts a list of SLAInstance objects"""
        if not sla_list:
            return
        session = self.Session()
        try:
            session.bulk_save_objects(sla_list)
            session.commit()
        except Exception as e:
            session.rollback()
            print(f"⚠️ Error creating bulk SLAs: {e}")
        finally:
            session.close()
