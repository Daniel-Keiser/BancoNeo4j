import uuid
from neo4j import GraphDatabase, Record

from datetime import datetime


from fastapi import FastAPI, HTTPException, Query, Path
from starlette.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware
from config import Neo4jSession  # Import the Neo4jSession class
from pydantic import BaseModel  # Import BaseModel from pydantic
from typing import List

import model as mdUser

# Graph2
app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Add your Vue.js application URL here
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create an instance of the Neo4jSession class
neo4j_session = Neo4jSession()

class UserCreate(BaseModel):
    username: str
    password: str
    first_name: str
    last_name: str
    gender: str

# Endpoint to create a new user in Neo4j
@app.post("/users", tags=["Users"])
def create_user(user_create: UserCreate):
    # Check if the user already exists
    query = f"MATCH (u:User {{username: '{user_create.username}'}}) RETURN u"
    with neo4j_session._driver.session() as session:
        result = session.run(query)
        existing_user = result.single()

    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    # Defina a data e hora atual
    create_at = datetime.utcnow()
    id = str(uuid.uuid4())

    # Create the user in Neo4j
    cypher_query = (
        f"CREATE (u:User {{"
        f"id: '{id}', "
        f"username: '{user_create.username}', "
        f"password: '{user_create.password}', "
        f"first_name: '{user_create.first_name}', "
        f"last_name: '{user_create.last_name}', "
        f"gender: '{user_create.gender}', "
        f"create_at: '{create_at.isoformat()}'"
        f"}})"
    )

    with neo4j_session._driver.session() as session:
        session.run(cypher_query)

    return JSONResponse(content={"message": "User created successfully"}, status_code=200)

@app.get("/users", response_model=List[mdUser.User], tags=["Users"])
def get_all_users_neo4j():
    # Consultar todos os usuários no Neo4j
    query = "MATCH (u:User) RETURN u.id, u.username, u.first_name, u.last_name, u.gender"
    
    with neo4j_session._driver.session() as session:
        result = session.run(query)
        users = result.data()

    if not users:
        raise HTTPException(status_code=404, detail="No users found in Neo4j")

    # Transformar os dados brutos em um formato mais limpo
    cleaned_users = [{"id": user["u.id"], "username": user["u.username"], "first_name": user["u.first_name"], "last_name": user["u.last_name"], "gender": user['u.gender']} for user in users]

    return cleaned_users


# Endpoint para obter um usuário pelo ID no Neo4j
@app.get("/users/{user_id}", response_model=mdUser.UserList, tags=["Users"])
def find_user_by_id(user_id: str):
    # Consultar o usuário no Neo4j pelo ID
    query = f"MATCH (u:User {{id: '{user_id}'}}) RETURN u"
    with neo4j_session._driver.session() as session:
        result = session.run(query)
        user = result.single()

    if user is None or not user['u']:
        raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found in Neo4j")

    # Extrair diretamente as propriedades do nó do usuário do resultado
    user_properties = dict(user['u'])

    # Remover a chave 'id' se você já tem o ID no path do endpoint
    user_properties.pop('id', None)

    # Retornar as propriedades do usuário como JSON
    return JSONResponse(content=user_properties, status_code=200)

# Endpoint para atualizar um usuário pelo ID no Neo4j
@app.put("/users", response_model=mdUser.UserList, tags=["Users"])
async def update_user(user: mdUser.UserUpdate):
    # Verificar se o usuário existe no Neo4j pelo ID
    check_query = f"MATCH (u:User {{id: '{user.id}'}}) RETURN u"
    with neo4j_session._driver.session() as check_session:
        check_result = check_session.run(check_query)
        existing_user = check_result.single()

    if existing_user is None:
        raise HTTPException(status_code=404, detail=f"User with ID {user.id} not found in Neo4j")

    # Construir a string Cypher para atualizar as propriedades do nó do usuário
    update_query = f"""
    MATCH (u:User {{id: '{user.id}'}})
    SET
      u.username = '{user.username}',
      u.first_name = '{user.first_name}',
      u.last_name = '{user.last_name}',
      u.gender = '{user.gender}',
      u.status = '{user.status}'
    RETURN u
    """
    with neo4j_session._driver.session() as update_session:
        update_result = update_session.run(update_query)
        updated_user_node = update_result.single()

    # Extrair diretamente as propriedades do nó do usuário atualizado
    updated_user_properties = dict(updated_user_node['u'])

    # Remover a chave 'id' se você já tem o ID no objeto do usuário
    updated_user_properties.pop('id', None)

    # Retornar as propriedades do usuário atualizado como JSON
    return JSONResponse(content=updated_user_properties, status_code=200)

# Endpoint para deletar um usuário pelo ID no Neo4j
@app.delete("/users/{user_id}", tags=["Users"])
def delete_user(user_id: str):
    # Consultar o usuário no Neo4j pelo ID para verificar se ele existe
    check_query = f"MATCH (u:User {{id: '{user_id}'}}) RETURN u"
    with neo4j_session._driver.session() as session:
        result = session.run(check_query)
        existing_user = result.single()

    if existing_user is None:
        raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found in Neo4j")

    # Executar a consulta de exclusão no Neo4j
    delete_query = f"MATCH (u:User {{id: '{user_id}'}}) DELETE u"
    with neo4j_session._driver.session() as session:
        session.run(delete_query)

    return {"message": f"Usuário com ID {user_id} foi excluído com sucesso."}


# Endpoint para criar uma especialidade no Neo4j
@app.post("/specialties/", response_model=mdUser.Specialty, tags=["Specialty"])
async def create_specialty(specialty: mdUser.SpecialtyCreate):
    query = (
        f"CREATE (s:Specialty {{id: '{str(uuid.uuid1())}', name: '{specialty.name}'}}) "
        "RETURN s.id, s.name"
    )

    with neo4j_session._driver.session() as session:
        result = session.run(query)
        created_specialty = result.single()

    if not created_specialty:
        raise HTTPException(status_code=500, detail="Falha ao criar especialidade no Neo4j")

    # Extrair os dados do nó Neo4j
    specialty_id, specialty_name = created_specialty

    # Construir uma resposta JSON
    response_data = {"id": specialty_id, "name": specialty_name}

    return JSONResponse(content=response_data, status_code=200)

# Endpoint para recuperar todas as especialidades do Neo4j
@app.get("/specialties/", response_model=List[mdUser.Specialty], tags=["Specialty"])
def get_specialties():
    # Consulta para obter todas as especialidades
    query = "MATCH (s:Specialty) RETURN s.id, s.name"

    # Execute a consulta no Neo4j
    with neo4j_session._driver.session() as session:
        result = session.run(query)
        specialties = [{"id": record["s.id"], "name": record["s.name"]} for record in result if record["s.id"] and record["s.name"]]

    if not specialties:
        return JSONResponse(content=[], status_code=200)

    return JSONResponse(content=specialties, status_code=200)


# Endpoint para excluir uma especialidade do Neo4j usando UUID
@app.delete("/specialties/{specialty_id}/", tags=["Specialty"])
def delete_specialty(specialty_id: str):
    # Verifique se a especialidade existe no Neo4j
    query_check_existence = f"MATCH (s:Specialty {{id: '{specialty_id}'}}) RETURN s"
    
    with neo4j_session._driver.session() as session:
        result = session.run(query_check_existence)
        existing_specialty = result.single()

    if not existing_specialty:
        raise HTTPException(status_code=404, detail=f"Specialty with ID {specialty_id} not found in Neo4j")

    # Exclua a especialidade no Neo4j
    query_delete = f"MATCH (s:Specialty {{id: '{specialty_id}'}}) DETACH DELETE s"

    with neo4j_session._driver.session() as session:
        session.run(query_delete)

    return JSONResponse(content={"message": "Specialty deleted successfully"}, status_code=200)


# Substitua 'bolt://localhost:7687' e 'your_password' pelos seus valores reais
neo4j_driver = GraphDatabase.driver('bolt://localhost:7687', auth=('neo4j', '12345678'))

def convert_node_to_dict(node):
    return {key: value for key, value in node.items()}

# Função para criar um médico no Neo4j
@app.post("/doctors/", response_model=mdUser.DoctorCreate, tags=["Doctors"])
def create_doctor(doctor: mdUser.DoctorCreate):
    # ... (verificação de existência de usuário e especialidade)

    # Gere um UUID para o ID do médico
    doctor_id = str(uuid.uuid4())

    query_create_doctor = (
        f"MATCH (u:User {{id: '{doctor.user_id}'}}) "
        f"MATCH (s:Specialty {{id: '{doctor.specialization_id}'}}) "
        f"CREATE (d:Doctor {{"
        f"id: '{doctor_id}', "
        f"user_id: '{doctor.user_id}', "
        f"specialization_id: '{doctor.specialization_id}'"
        f"}})-[:IS_USER]->(u) "
        f"CREATE (d)-[:HAS_SPECIALIZATION]->(s) "
        f"RETURN d, u, s"
    )

    with neo4j_session._driver.session() as session:
        result = session.run(query_create_doctor)
        created_doctor = result.single()["d"]

    # Converta o objeto Node em um dicionário para ser serializado para JSON
    created_doctor_dict = convert_node_to_dict(created_doctor)

    # Retorne os dados do médico criado, incluindo o ID gerado automaticamente
    return JSONResponse(content=created_doctor_dict, status_code=201)

def record_to_dict(record):
    return {key: record[key] for key in record.keys()}


@app.get("/doctors/", response_model=List[mdUser.DoctorWithDetails], tags=["Doctors"])
def get_doctors():
    # Consulta Cypher para obter todos os médicos
    query = (
        "MATCH (d:Doctor) "
        "OPTIONAL MATCH (d)-[:IS_USER]->(u:User) "
        "OPTIONAL MATCH (d)-[:HAS_SPECIALIZATION]->(s:Specialty) "
        "WITH d, COLLECT(DISTINCT u) AS users, COLLECT(DISTINCT s) AS specialties "
        "RETURN d, users, specialties"
    )

    with neo4j_session._driver.session() as session:
        result = session.run(query)
        doctor_details_list = []

        for record in result:
            doctor_node = record["d"]
            user_nodes = record["users"]
            specialty_nodes = record["specialties"]

            for user_node in user_nodes:
                doctor_details = {
                    "doctor_id": str(doctor_node["id"]) if doctor_node and "id" in doctor_node else None,
                    "user_id": str(user_node["id"]) if user_node and "id" in user_node else None,
                    "specialization_id": str(specialty_nodes[0]["id"]) if specialty_nodes and specialty_nodes[0] and "id" in specialty_nodes[0] else None,
                    "specialization_name": specialty_nodes[0]["name"] if specialty_nodes and specialty_nodes[0] else None,
                    "username": user_node["username"] if user_node and "username" in user_node else None,
                }

                doctor_details_list.append(doctor_details)

    if not doctor_details_list:
        raise HTTPException(status_code=404, detail="Nenhum médico encontrado")

    return doctor_details_list

@app.get("/patients/{patient_id}", response_model=List[mdUser.PatientWithUserDetails], tags=["Patients"])
def get_patient(patient_id: str = Path(..., title="ID do Paciente", description="ID único do paciente a ser consultado")):
    # Consulta Cypher para obter o paciente específico e seus detalhes relacionados ao usuário
    query = (
        f"MATCH (p:Patient {{id: '{patient_id}'}})-[:IS_USERP]->(u:User) "
        "RETURN p, u"
    )

    with neo4j_session._driver.session() as session:
        result = session.run(query)
        patient_details_list = []

        for record in result:
            patient_node = record["p"]
            user_node = record["u"]

            patient_details = {
                "patient_id": str(patient_node["id"]) if patient_node and "id" in patient_node else None,
                "user_id": str(user_node["id"]) if user_node and "id" in user_node else None,
                "medical_history": patient_node["medical_history"] if patient_node else None,
                "contact_emergency": patient_node["contact_emergency"] if patient_node else None,
                "address": patient_node["address"] if patient_node else None,
                "phone_number": patient_node["phone_number"] if patient_node else None,
                "age": patient_node["age"] if patient_node else None,
                "username": user_node["username"] if user_node else None,
                "first_name": user_node["first_name"] if user_node else None,
                "last_name": user_node["last_name"] if user_node else None,
            }

            patient_details_list.append(patient_details)

    if not patient_details_list:
        raise HTTPException(status_code=404, detail=f"Paciente com ID {patient_id} não encontrado")

    return patient_details_list



@app.delete("/doctors/{doctor_id}", response_model=dict, tags=["Doctors"])
def delete_doctor(doctor_id: str):
    # Consultar o médico no Neo4j pelo ID
    query_find_doctor = f"MATCH (d:Doctor {{id: '{doctor_id}'}}) RETURN d"
    with neo4j_session._driver.session() as session:
        result = session.run(query_find_doctor)
        doctor = result.single()

    # Verificar se o médico existe no Neo4j
    if doctor is None:
        raise HTTPException(status_code=404, detail=f"Doctor with ID {doctor_id} not found in Neo4j")

    # Excluir o médico no Neo4j
    query_delete_doctor = f"MATCH (d:Doctor {{id: '{doctor_id}'}}) DETACH DELETE d"
    with neo4j_session._driver.session() as session:
        session.run(query_delete_doctor)

    return {"status": True, "message": f"Doctor with ID {doctor_id} has been deleted successfully in Neo4j."}

# Endpoint para criar um paciente no Neo4j
@app.post("/patients/", response_model=mdUser.PatientCreate, tags=["Patients"])
async def create_patient(patient: mdUser.PatientCreate):
    # Crie o nó do paciente no Neo4j com um UUID

    id = str(uuid.uuid4())
        
    query_create_patient = (
        f"MATCH (u:User {{id: '{patient.user_id}'}}) "
        f"CREATE (p:Patient {{"
        f"id: '{id}', "
        f"user_id: '{patient.user_id}', "
        f"medical_history: '{patient.medical_history}', "
        f"contact_emergency: '{patient.contact_emergency}', "
        f"address: '{patient.address}', "
        f"phone_number: '{patient.phone_number}', "
        f"age: {patient.age}"
        f"}})-[:IS_USERP]->(u)"
        f"RETURN p, u"
    )

    with neo4j_session._driver.session() as session:
        result = session.run(query_create_patient)
        created_patient = result.single()["p"]

    # Converta o objeto Node em um dicionário para ser serializado para JSON
    created_patient_dict = dict(created_patient)

    # Retorne os dados do paciente criado
    return created_patient_dict


@app.get("/patients/", response_model=List[mdUser.PatientWithUserDetails], tags=["Patients"])
def get_patients():
    # Consulta Cypher para obter todos os pacientes e seus detalhes relacionados aos usuários
    query = (
        "MATCH (p:Patient)-[:IS_USERP]->(u:User) "
        "RETURN p, u"
    )

    with neo4j_session._driver.session() as session:
        result = session.run(query)
        patient_details_list = []

        for record in result:
            patient_node = record["p"]
            user_node = record["u"]

            patient_details = {
                "patient_id": str(patient_node["id"]) if patient_node and "id" in patient_node else None,
                "user_id": str(user_node["id"]) if user_node and "id" in user_node else None,
                "medical_history": patient_node["medical_history"] if patient_node else None,
                "contact_emergency": patient_node["contact_emergency"] if patient_node else None,
                "address": patient_node["address"] if patient_node else None,
                "phone_number": patient_node["phone_number"] if patient_node else None,
                "age": patient_node["age"] if patient_node else None,
                "username": user_node["username"] if user_node else None,
                "first_name": user_node["first_name"] if user_node else None,
                "last_name": user_node["last_name"] if user_node else None,
            }

            patient_details_list.append(patient_details)

    if not patient_details_list:
        raise HTTPException(status_code=404, detail="Nenhum paciente encontrado")

    return patient_details_list

@app.get("/patients/", response_model=List[mdUser.PatientWithUserDetails], tags=["Patients"])
def get_patients(patient_id: str = Query(None, title="Patient ID", description="ID do paciente para consulta individual")):
    # Consulta Cypher para obter pacientes e seus detalhes relacionados aos usuários
    if patient_id:
        query = (
            "MATCH (p:Patient {id: $patient_id})-[:IS_USERP]->(u:User) "
            "RETURN p, u"
        )
        parameters = {"patient_id": patient_id}
    else:
        query = (
            "MATCH (p:Patient)-[:IS_USERP]->(u:User) "
            "RETURN p, u"
        )
        parameters = {}

    with neo4j_session._driver.session() as session:
        result = session.run(query, parameters)
        patient_details_list = []

        for record in result:
            patient_node = record["p"]
            user_node = record["u"]

            patient_details = {
                "patient_id": str(patient_node["id"]) if patient_node and "id" in patient_node else None,
                "user_id": str(user_node["id"]) if user_node and "id" in user_node else None,
                "medical_history": patient_node["medical_history"] if patient_node else None,
                "contact_emergency": patient_node["contact_emergency"] if patient_node else None,
                "address": patient_node["address"] if patient_node else None,
                "phone_number": patient_node["phone_number"] if patient_node else None,
                "age": patient_node["age"] if patient_node else None,
                "username": user_node["username"] if user_node else None,
                "first_name": user_node["first_name"] if user_node else None,
                "last_name": user_node["last_name"] if user_node else None,
            }

            patient_details_list.append(patient_details)

    if not patient_details_list:
        raise HTTPException(status_code=404, detail="Nenhum paciente encontrado")

    return patient_details_list

@app.get("/patients/{patient_id}", response_model=List[mdUser.PatientWithUserDetails], tags=["Patients"])
def get_patient(patient_id: str = Path(..., title="ID do Paciente", description="ID único do paciente a ser consultado")):
    # Consulta Cypher para obter o paciente específico e seus detalhes relacionados ao usuário
    query = (
        f"MATCH (p:Patient {{id: '{patient_id}'}})-[:IS_USERP]->(u:User) "
        "RETURN p, u"
    )

    with neo4j_session._driver.session() as session:
        result = session.run(query)
        patient_details_list = []

        for record in result:
            patient_node = record["p"]
            user_node = record["u"]

            patient_details = {
                "patient_id": str(patient_node["id"]) if patient_node and "id" in patient_node else None,
                "user_id": str(user_node["id"]) if user_node and "id" in user_node else None,
                "medical_history": patient_node["medical_history"] if patient_node else None,
                "contact_emergency": patient_node["contact_emergency"] if patient_node else None,
                "address": patient_node["address"] if patient_node else None,
                "phone_number": patient_node["phone_number"] if patient_node else None,
                "age": patient_node["age"] if patient_node else None,
                "username": user_node["username"] if user_node else None,
                "first_name": user_node["first_name"] if user_node else None,
                "last_name": user_node["last_name"] if user_node else None,
            }

            patient_details_list.append(patient_details)

    if not patient_details_list:
        raise HTTPException(status_code=404, detail=f"Paciente com ID {patient_id} não encontrado")

    return patient_details_list

@app.delete("/patients/{patient_id}", response_model=dict, tags=["Patients"])
def delete_patient(patient_id: str = Path(..., title="ID do Paciente", description="ID único do paciente a ser deletado")):
    # Consulta Cypher para deletar o paciente específico
    query = (
        f"MATCH (p:Patient {{id: '{patient_id}'}})-[r]-() "
        "DELETE p, r"
    )

    with neo4j_session._driver.session() as session:
        result = session.run(query)

    # Verifica se algum paciente foi deletado
    if result.summary().counters.nodes_deleted == 0:
        raise HTTPException(status_code=404, detail=f"Paciente com ID {patient_id} não encontrado")

    return {"message": f"Paciente com ID {patient_id} deletado com sucesso"}

@app.patch("/patients/{patient_id}", response_model=mdUser.PatientWithUserDetails, tags=["Patients"])
def update_patient(
    update_data: mdUser.PatientUpdate,
    patient_id: str = Path(..., title="ID do Paciente", description="ID único do paciente a ser atualizado"),
):
    # Lógica para atualizar o paciente no Neo4j
    query = (
        f"MATCH (p:Patient {{id: '{patient_id}'}}) "
        "SET "
        f"p.medical_history = COALESCE('{update_data.medical_history}', p.medical_history), "
        f"p.contact_emergency = COALESCE('{update_data.contact_emergency}', p.contact_emergency), "
        f"p.address = COALESCE('{update_data.address}', p.address), "
        f"p.phone_number = COALESCE('{update_data.phone_number}', p.phone_number), "
        f"p.age = {update_data.age} "
        "RETURN p"
    )

    with neo4j_session._driver.session() as session:
        result = session.run(query)
        updated_patient = result.single()["p"]

    # Lógica para obter informações do usuário relacionado
    user_query = (
        f"MATCH (p:Patient {{id: '{patient_id}'}})-[:IS_USERP]->(u:User) "
        "RETURN u"
    )

    with neo4j_session._driver.session() as session:
        result = session.run(user_query)
        user_node = result.single()["u"]

    # Construa a resposta final com informações do paciente e do usuário
    patient_details = {
        "patient_id": str(updated_patient["id"]),
        "user_id": str(user_node["id"]) if user_node else None,
        "medical_history": updated_patient["medical_history"],
        "contact_emergency": updated_patient["contact_emergency"],
        "address": updated_patient["address"],
        "phone_number": updated_patient["phone_number"],
        "age": updated_patient["age"],
        "username": user_node["username"] if user_node else None,
        "first_name": user_node["first_name"] if user_node else None,
        "last_name": user_node["last_name"] if user_node else None,
    }

    return patient_details

@app.post("/appointment-statuses/", response_model=mdUser.Status, tags=["Status"])
async def create_appointment_status(status_name: str = Query(..., title="Status Name", description="Name of the appointment status")):
    query = (
        f"CREATE (s:Status {{id: '{str(uuid.uuid1())}', name: '{status_name}'}}) "
        "RETURN s.id, s.name"
    )

    with neo4j_session._driver.session() as session:
        result = session.run(query)
        created_status = result.single()

    if not created_status:
        raise HTTPException(status_code=500, detail="Failed to create status in Neo4j")

    # Extract data from Neo4j node
    status_id, status_name = created_status

    # Build JSON response
    response_data = {"id": status_id, "name": status_name}

    return response_data

@app.get("/appointment-statuses/", response_model=List[mdUser.Status], tags=["Status"])
async def get_appointment_statuses():
    query = (
        "MATCH (s:Status) "
        "RETURN s.id, s.name"
    )

    with neo4j_session._driver.session() as session:
        result = session.run(query)
        statuses = [{"id": record["s.id"], "name": record["s.name"]} for record in result if record["s.id"] and record["s.name"]]

    return statuses

@app.delete("/appointment-statuses/{status_id}", tags=["Status"])
async def delete_appointment_status(status_id: str):
    # Verificar se o status existe antes de tentar deletar
    check_query = f"MATCH (s:Status {{id: '{status_id}'}}) RETURN s.id, s.name"
    
    with neo4j_session._driver.session() as check_session:
        check_result = check_session.run(check_query)
        existing_status = check_result.single()

    if not existing_status:
        raise HTTPException(status_code=404, detail=f"Status com ID {status_id} não encontrado")

    # Deletar o status
    delete_query = f"MATCH (s:Status {{id: '{status_id}'}}) DETACH DELETE s"
    
    with neo4j_session._driver.session() as delete_session:
        delete_session.run(delete_query)

    # Retornar uma mensagem de sucesso
    return {"message": f"Status com ID {status_id} deletado com sucesso"}

def generate_uuid():
    return str(uuid.uuid4())

@app.post("/appointments/", response_model=mdUser.AppointmentCreate, tags=["Appointments"])
def create_appointment(appointment_data: mdUser.AppointmentCreate):
    # Gere um UUID para o ID do compromisso
    appointment_id = generate_uuid()

    # Crie o nó do compromisso no Neo4j
    query_create_appointment = (
        f"MATCH (patient:Patient {{id: '{appointment_data.patient_id}'}}) "
        f"MATCH (doctor:Doctor {{id: '{appointment_data.doctor_id}'}}) "
        f"MATCH (specialty:Specialty {{id: '{appointment_data.specialty_id}'}}) "
        f"MATCH (status:Status {{id: '{appointment_data.status_id}'}}) "
        f"CREATE (a:Appointment {{"
        f"id: '{appointment_id}', "
        f"appointment_datetime: '{appointment_data.appointment_datetime}', "
        f"observations: '{appointment_data.observations}', "
        f"duration: '{appointment_data.duration}'"
        f"}})-[:HAS_APPOINTMENT]->(patient), "
        f"(a)-[:HAS_APPOINTMENT]->(doctor), "
        f"(a)-[:HAS_APPOINTMENT]->(specialty), "
        f"(a)-[:HAS_APPOINTMENT]->(status) "
        f"RETURN a"
    )

    with neo4j_session._driver.session() as session:
        result = session.run(query_create_appointment)
        created_appointment = result.single()["a"]

    # Converta o objeto Node em um dicionário para ser serializado para JSON
    created_appointment_dict = convert_node_to_dict(created_appointment)

    # Retorne os dados do médico criado, incluindo o ID gerado automaticamente
    return JSONResponse(content=created_appointment_dict, status_code=201)

@app.get("/medical_appointments/", tags=["Appointments"])
def get_medical_appointments():
    query = (
        "MATCH (a:Appointment)-[:HAS_APPOINTMENT]->(status:Status) "
        "MATCH (a)-[:HAS_APPOINTMENT]->(specialty:Specialty) "
        "MATCH (a)-[:HAS_APPOINTMENT]->(doctor:Doctor)-[:IS_USER]->(doctorUser:User) "
        "MATCH (a)-[:HAS_APPOINTMENT]->(patient:Patient)-[:IS_USERP]->(patientUser:User) "
        "RETURN "
        "a, "
        "status, "
        "specialty, "
        "doctor, "
        "doctorUser.username AS doctor_username, "
        "doctorUser.first_name AS doctor_first_name, "
        "doctorUser.last_name AS doctor_last_name, "
        "patient, "
        "patientUser.username AS patient_username, "
        "patientUser.first_name AS patient_first_name, "
        "patientUser.last_name AS patient_last_name, "
        "status.name AS status_name, "
        "specialty.name AS specialty_name, "
        "a.duration AS duration, " 
        "a.observations AS observations, " 
        "a.appointment_datetime AS appointment_datetime"
    )

    with neo4j_session._driver.session() as session:
        result: Result = session.run(query)
        medical_appointments_list = []

        for record in result:
            appointment_node = record["a"]
            status_node = record["status"]
            specialty_node = record["specialty"]
            doctor_node = record["doctor"]
            patient_node = record["patient"]
            doctor_username = record["doctor_username"]
            doctor_first_name = record["doctor_first_name"]
            doctor_last_name = record["doctor_last_name"]
            patient_username = record["patient_username"]
            patient_first_name = record["patient_first_name"]
            patient_last_name = record["patient_last_name"]
            status_name = record["status_name"]
            specialty_name = record["specialty_name"]
            duration = record["duration"]
            observations = record["observations"]
            appointment_datetime = record["appointment_datetime"]

            medical_appointment_details = {
                "appointment_id": str(appointment_node["id"]) if appointment_node and "id" in appointment_node else None,
                "status_id": str(status_node["id"]) if status_node and "id" in status_node else None,
                "status_name": status_name,
                "specialty_id": str(specialty_node["id"]) if specialty_node and "id" in specialty_node else None,
                "specialty_name": specialty_name,
                "doctor_id": str(doctor_node["id"]) if doctor_node and "id" in doctor_node else None,
                "doctor_username": doctor_username,
                "doctor_first_name": doctor_first_name,
                "doctor_last_name": doctor_last_name,
                "patient_id": str(patient_node["id"]) if patient_node and "id" in patient_node else None,
                "patient_username": patient_username,
                "patient_first_name": patient_first_name,
                "patient_last_name": patient_last_name,
                "duration": duration,
                "observations": observations,
                "appointment_datetime": appointment_datetime,
            }

            medical_appointments_list.append(medical_appointment_details)

    if not medical_appointments_list:
        raise HTTPException(status_code=404, detail="Nenhum compromisso médico encontrado")

    return medical_appointments_list

@app.get("/medical_appointments/{appointment_id}", tags=["Appointments"])
def get_medical_appointment(appointment_id: str = Path(..., title="ID do Compromisso Médico")):
    query = (
        "MATCH (a:Appointment {id: $appointment_id})-[:HAS_APPOINTMENT]->(status:Status) "
        "MATCH (a)-[:HAS_APPOINTMENT]->(specialty:Specialty) "
        "MATCH (a)-[:HAS_APPOINTMENT]->(doctor:Doctor)-[:IS_USER]->(doctorUser:User) "
        "MATCH (a)-[:HAS_APPOINTMENT]->(patient:Patient)-[:IS_USERP]->(patientUser:User) "
        "RETURN "
        "a, "
        "status, "
        "specialty, "
        "doctor, "
        "doctorUser.username AS doctor_username, "
        "doctorUser.first_name AS doctor_first_name, "
        "doctorUser.last_name AS doctor_last_name, "
        "patient, "
        "patientUser.username AS patient_username, "
        "patientUser.first_name AS patient_first_name, "
        "patientUser.last_name AS patient_last_name, "
        "status.name AS status_name, "
        "specialty.name AS specialty_name, "
        "a.duration AS duration, " 
        "a.observations AS observations, " 
        "a.appointment_datetime AS appointment_datetime"
    )

    with neo4j_session._driver.session() as session:
        result: Result = session.run(query, appointment_id=appointment_id)
        record = result.single()

        if not record:
            raise HTTPException(status_code=404, detail="Compromisso médico não encontrado")

        appointment_node = record["a"]
        status_node = record["status"]
        specialty_node = record["specialty"]
        doctor_node = record["doctor"]
        patient_node = record["patient"]
        doctor_username = record["doctor_username"]
        doctor_first_name = record["doctor_first_name"]
        doctor_last_name = record["doctor_last_name"]
        patient_username = record["patient_username"]
        patient_first_name = record["patient_first_name"]
        patient_last_name = record["patient_last_name"]
        status_name = record["status_name"]
        specialty_name = record["specialty_name"]
        duration = record["duration"]
        observations = record["observations"]
        appointment_datetime = record["appointment_datetime"]

        medical_appointment_details = {
            "appointment_id": str(appointment_node["id"]) if appointment_node and "id" in appointment_node else None,
            "status_id": str(status_node["id"]) if status_node and "id" in status_node else None,
            "status_name": status_name,
            "specialty_id": str(specialty_node["id"]) if specialty_node and "id" in specialty_node else None,
            "specialty_name": specialty_name,
            "doctor_id": str(doctor_node["id"]) if doctor_node and "id" in doctor_node else None,
            "doctor_username": doctor_username,
            "doctor_first_name": doctor_first_name,
            "doctor_last_name": doctor_last_name,
            "patient_id": str(patient_node["id"]) if patient_node and "id" in patient_node else None,
            "patient_username": patient_username,
            "patient_first_name": patient_first_name,
            "patient_last_name": patient_last_name,
            "duration": duration,
            "observations": observations,
            "appointment_datetime": appointment_datetime,
        }

    return medical_appointment_details

@app.delete("/medical_appointments/{appointment_id}", tags=["Appointments"])
def delete_medical_appointment(appointment_id: str = Path(..., title="ID do Compromisso Médico")):
    # Consulta Cypher para deletar o compromisso médico com base no ID
    query = (
        "MATCH (a:Appointment {id: $appointment_id}) "
        "DETACH DELETE a"
    )

    with neo4j_session._driver.session() as session:
        result = session.run(query, appointment_id=appointment_id)

        # Verifica se algum nó foi deletado (result.summary().counters.nodes_deleted)
        if result.summary().counters.nodes_deleted == 0:
            raise HTTPException(status_code=404, detail="Compromisso médico não encontrado")

    return {"message": f"Compromisso médico com ID {appointment_id} deletado com sucesso"}

class UpdateMedicalAppointmentModel(BaseModel):
    duration: str
    appointment_datetime: str
    observations: str

@app.patch("/medical_appointments/{appointment_id}", tags=["Appointments"])
def update_medical_appointment(
    update_data: UpdateMedicalAppointmentModel,
    appointment_id: str = Path(..., title="ID do Compromisso Médico"),
):
    # Consulta Cypher para atualizar o compromisso médico com base no ID
    query = (
        "MATCH (a:Appointment {id: $appointment_id}) "
        "SET a.duration = $duration, "
        "a.appointment_datetime = $appointment_datetime, "
        "a.observations = $observations "
        "RETURN a"
    )

    with neo4j_session._driver.session() as session:
        result = session.run(
            query,
            appointment_id=appointment_id,
            duration=update_data.duration,
            appointment_datetime=update_data.appointment_datetime,
            observations=update_data.observations
        )

        # Obtém o primeiro nó da resposta
        updated_appointment = result.single()

        # Verifica se algum nó foi encontrado
        if updated_appointment is None:
            raise HTTPException(status_code=404, detail="Compromisso médico não encontrado")

        # Converte o nó em um dicionário para serialização JSON
        updated_appointment_dict = convert_node_to_dict(updated_appointment["a"])

    return updated_appointment_dict

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
