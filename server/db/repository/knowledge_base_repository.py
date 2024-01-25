from server.db.models.knowledge_base_model import KnowledgeBaseModel
from server.db.session import with_session


@with_session
def add_kb_to_db(session, kb_name, kb_info, vs_type, embed_model, endpoint_host: str = None,
                 endpoint_host_key: str = None, endpoint_host_proxy: str = None):
    # 创建知识库实例
    kb = session.query(KnowledgeBaseModel).filter(KnowledgeBaseModel.kb_name.ilike(kb_name)).first()
    if not kb:
        kb = KnowledgeBaseModel(kb_name=kb_name, kb_info=kb_info, vs_type=vs_type, embed_model=embed_model,
                                endpoint_host=endpoint_host, endpoint_host_key=endpoint_host_key,
                                endpoint_host_proxy=endpoint_host_proxy)
        session.add(kb)
    else:  # update kb with new vs_type and embed_model
        kb.kb_info = kb_info
        kb.vs_type = vs_type
        kb.embed_model = embed_model
        kb.endpoint_host = endpoint_host
        kb.endpoint_host_key = endpoint_host_key
        kb.endpoint_host_proxy = endpoint_host_proxy
    return True


@with_session
def list_kbs_from_db(session, min_file_count: int = -1):
    kbs = session.query(KnowledgeBaseModel.kb_name).filter(KnowledgeBaseModel.file_count > min_file_count).all()
    kbs = [kb[0] for kb in kbs]
    return kbs


@with_session
def kb_exists(session, kb_name):
    kb = session.query(KnowledgeBaseModel).filter(KnowledgeBaseModel.kb_name.ilike(kb_name)).first()
    status = True if kb else False
    return status


@with_session
def load_kb_from_db(session, kb_name):
    kb = session.query(KnowledgeBaseModel).filter(KnowledgeBaseModel.kb_name.ilike(kb_name)).first()
    if kb:
        kb_name, vs_type, embed_model = kb.kb_name, kb.vs_type, kb.embed_model
    else:
        kb_name, vs_type, embed_model = None, None, None
    return kb_name, vs_type, embed_model


@with_session
def delete_kb_from_db(session, kb_name):
    kb = session.query(KnowledgeBaseModel).filter(KnowledgeBaseModel.kb_name.ilike(kb_name)).first()
    if kb:
        session.delete(kb)
    return True


@with_session
def update_kb_endpoint_from_db(session, kb_name, endpoint_host, endpoint_host_key, endpoint_host_proxy):
    kb = session.query(KnowledgeBaseModel).filter_by(kb_name=kb_name).first()
    if kb:
        kb.endpoint_host = endpoint_host
        kb.endpoint_host_key = endpoint_host_key
        kb.endpoint_host_proxy = endpoint_host_proxy
    return True


@with_session
def get_kb_detail(session, kb_name: str) -> dict:
    kb: KnowledgeBaseModel = session.query(KnowledgeBaseModel).filter(KnowledgeBaseModel.kb_name.ilike(kb_name)).first()
    if kb:
        return {
            "kb_name": kb.kb_name,
            "kb_info": kb.kb_info,
            "vs_type": kb.vs_type,
            "endpoint_host": kb.endpoint_host,
            "endpoint_host_key": kb.endpoint_host_key,
            "endpoint_host_proxy": kb.endpoint_host_proxy,
            "embed_model": kb.embed_model,
            "file_count": kb.file_count,
            "create_time": kb.create_time,
        }
    else:
        return {}
