import pymongo
import gridfs
import re
import os
import sys
from datetime import datetime
import ruamel.yaml
import traceback
import atexit
import magic
import math
yaml = ruamel.yaml.YAML(typ="safe")
yaml.default_flow_style = False

global GLOBAL_schema_version
GLOBAL_schema_version = 2.0

def date_now():
    """
    Needed to keep the same date in python and mongo, as mongo rounds to millisecond
    """
    d = datetime.utcnow()
    return d.replace(microsecond=math.floor(d.microsecond/1000)*1000)

CONNECTION = None

def close_connection():
    global CONNECTION
    if CONNECTION is not None:
        CONNECTION.close()

atexit.register(close_connection)


def get_connection():
    global CONNECTION
    if CONNECTION is not None:
        return CONNECTION
    else:
        if os.getenv("BIFROST_DB_KEY", None) is not None:
            CONNECTION = pymongo.MongoClient(os.getenv("BIFROST_DB_KEY"))  # Note none here apparently will use defaults which means localhost:27017
            return CONNECTION
        else:
            raise ValueError("BIFROST_DB_KEY not set")



def dump_run_info(data_dict):
    """Insert sample dict into mongodb.
    Return the dict with an _id element"""
    connection = get_connection()
    db = connection.get_database()
    runs_db = db.runs  # Collection name is samples
    now = date_now()
    data_dict["metadata"] = data_dict.get("metadata", {"schema_version": GLOBAL_schema_version, "created_at": now})
    data_dict["metadata"]["updated_at"] = now
    if "_id" in data_dict and data_dict["_id"] is not None:
        data_dict = runs_db.find_one_and_update(
            filter={"_id": data_dict["_id"]},
            update={"$set": data_dict},
            return_document=pymongo.ReturnDocument.AFTER,  # return new doc if one is upserted
            upsert=True  # This might change in the future  # insert the document if it does not exist
        )
    else:
        result = runs_db.insert_one(data_dict)
        data_dict["_id"] = result.inserted_id

    return data_dict

def delete_run(run_id):
    connection = get_connection()
    db = connection.get_database()
    deleted = db.runs.delete_one({"_id": run_id})
    return deleted.deleted_count


def dump_sample_info(data_dict):
    """Insert sample dict into mongodb.
    Return the dict with an _id element"""
    connection = get_connection()
    db = connection.get_database()
    samples_db = db.samples  # Collection name is samples
    now = date_now()
    data_dict["metadata"] = data_dict.get("metadata", {"schema_version": GLOBAL_schema_version, "created_at": now})
    data_dict["metadata"]["updated_at"] = now
    if "_id" in data_dict and data_dict["_id"] is not None:
        data_dict = samples_db.find_one_and_update(
            filter={"_id": data_dict["_id"]},
            update={"$set": data_dict},
            return_document=pymongo.ReturnDocument.AFTER,  # return new doc if one is upserted
            upsert=True  # This might change in the future  # insert the document if it does not exist
        )
    else:
        result = samples_db.insert_one(data_dict)
        data_dict["_id"] = result.inserted_id
    return data_dict


def get_components(component_ids=None, component_names=None, component_versions=None):
    """
    Return components based on query
    """
    query = []
    if component_ids is not None:
        query.append({"_id": {"$in": component_ids}})
    if component_names is not None:
        query.append({"name": {"$in": component_names}})
    if component_versions is not None:
        query.append({"version": {"$in": component_versions}})
    connection = get_connection()
    db = connection.get_database()
    if len(query) == 0:
        query = {}
    else:
        query = {"$and": query}
    return list(db.components.find(query).sort([("_id", pymongo.DESCENDING)]))


def dump_component_info(data_dict):
    """Insert sample dict into mongodb.
    Return the dict with an _id element"""
    connection = get_connection()
    db = connection.get_database()
    components_db = db.components  # Collection name is samples
    now = date_now()
    data_dict["metadata"] = data_dict.get("metadata", {"schema_version": GLOBAL_schema_version, "created_at": now})
    data_dict["metadata"]["updated_at"] = now
    if "_id" in data_dict and data_dict["_id"] is not None:
        data_dict = components_db.find_one_and_update(
            filter={"_id": data_dict["_id"]},
            update={"$set": data_dict},
            return_document=pymongo.ReturnDocument.AFTER,  # return new doc if one is upserted
            upsert=True  # This might change in the future # insert the document if it does not exist
        )
    else:
        data_dict = components_db.find_one_and_update(
            filter={"name": data_dict["name"], "version": data_dict["version"]},
            update={"$setOnInsert": data_dict},
            return_document=pymongo.ReturnDocument.AFTER,
            upsert=True
        )

    return data_dict

def delete_component(component_id):
    connection = get_connection()
    db = connection.get_database()
    deleted = db.components.delete_one({"_id": component_id})
    return deleted.deleted_count


def dump_sample_component_info(data_dict):
    """Insert sample dict into mongodb.
    Return the dict with an _id element"""
    connection = get_connection()
    db = connection.get_database()
    sample_components_db = db.sample_components  # Collection name is samples
    now = date_now()
    data_dict["metadata"] = data_dict.get("metadata", {"schema_version": GLOBAL_schema_version, "created_at": now})
    data_dict["metadata"]["updated_at"] = now
    if "_id" in data_dict:
        data_dict = sample_components_db.find_one_and_update(
            filter={"_id": data_dict["_id"]},
            update={"$set": data_dict},
            return_document=pymongo.ReturnDocument.AFTER,  # return new doc if one is upserted
            upsert=True  # This might change in the future. It doesnt make much sense with our current system.
            # Import relies on this to be true.
            # insert the document if it does not exist
        )
    else:
        search_fields = {
            "sample._id": data_dict["sample"]["_id"],
            "component._id": data_dict["component"]["_id"],
        }
        data_dict = sample_components_db.find_one_and_update(
            filter=search_fields,
            update={
                "$set": data_dict
            },
            return_document=pymongo.ReturnDocument.AFTER,  # return new doc if one is upserted
            upsert=True  # insert the document if it does not exist
        )
    return data_dict


# Should call get_species
def query_mlst_species(ncbi_species_name):
    if ncbi_species_name is None:
        return None
    try:
        connection = get_connection()
        db = connection.get_database('bifrost_species')
        species_db = db.species  # Collection name is samples
        result = species_db.find_one({"ncbi_species": ncbi_species_name}, {"mlst_species": 1, "_id": 0})
        if result is not None and "mlst_species" in result:
            return result["mlst_species"]
        else:
            return None
    except Exception:
        print(traceback.format_exc())
        return None


# Should call get_species
def query_ncbi_species(species_entry):
    if species_entry is None:
        return None
    try:
        connection = get_connection()
        db = connection.get_database('bifrost_species')
        species_db = db.species  # Collection name is samples
        result = species_db.find_one({"organism": species_entry}, {"ncbi_species": 1, "_id": 0})
        group_result = species_db.find_one({"group": species_entry}, {"ncbi_species": 1, "_id": 0})
        if result is not None:
            return result["ncbi_species"]
        elif group_result is not None:
            return group_result["ncbi_species"]
        else:
            return None
    except Exception:
        print(traceback.format_exc())
        return None


# Should be renamed to get_species
def query_species(ncbi_species_name):
    try:
        connection = get_connection()
        db = connection.get_database('bifrost_species')
        species_db = db.species
        if ncbi_species_name is not None and species_db.find({'ncbi_species': ncbi_species_name}).count() > 0:
            return species_db.find_one({"ncbi_species": ncbi_species_name})
        else:
            return species_db.find_one({"organism": "default"})
    except Exception:
        print(traceback.format_exc())
        return None


# DEPRECATED
def load_run(**kwargs):
    get_runs(**kwargs)


def get_runs(run_id=None,
             sample_id=None,
             names=None,
             size=0):

    size = min(1000, size)
    size = max(-1000, size)

    query = []

    try:
        connection = get_connection()
        db = connection.get_database()
        if names is not None:
            query.append({"name": {"$in": names}})
        if run_id is not None:
            query.append({"_id": run_id})
        if sample_id is not None:
            query.append({"sample._id": sample_id})
        if len(query) == 0:
            query = {}
        else:
            query = {"$and": query}
        return list(db.runs.find(
            query).sort([("_id", pymongo.DESCENDING)]).limit(size))
    except Exception:
        print(traceback.format_exc())
        return None


def get_samples(sample_ids=None, run_names=None, component_ids=None):
    # Uses AND operand

    query = []

    try:
        connection = get_connection()
        db = connection.get_database()

        if sample_ids is not None:
            query.append({"_id": {"$in": sample_ids}})
        if run_names is not None:
            run = db.runs.find_one({"name": {"$in": run_names}}, {"samples._id": 1})
            if run is not None:
                run_sample_ids = [s["_id"] for s in run["samples"]]
            else:
                run_sample_ids = []
            query.append({"_id": {"$in": run_sample_ids}})

        if component_ids is not None:
            query.append({"components._id": {"$in": component_ids}})

        if len(query) == 0:
            return list(db.samples.find({}))
        else:
            return list(db.samples.find({"$and": query}))
    except Exception:
        print(traceback.format_exc())
        return None


def get_sample_components(sample_component_ids=None,
                          sample_ids=None,
                          component_ids=None,
                          component_names=None,
                          size=0):
    """Loads most recent sample component for a sample"""
    size = min(1000, size)
    size = max(-1000, size)

    query = []
    if sample_component_ids is not None:
        query.append({"_id": {"$in": sample_component_ids}})
    if sample_ids is not None:
        query.append({"sample._id": {"$in": sample_ids}})
    if component_ids is not None:
        query.append({"component._id": {"$in": component_ids}})
    if component_names is not None:
        query.append({"component.name": {"$in": component_names}})
    try:
        connection = get_connection()
        db = connection.get_database()
        if len(query):
            query = {"$and": query}
        else:
            query = {}
        return list(db.sample_components.find(query)
                                        .sort([("setup_date", -1)])
                                        .limit(size))

    except Exception:
        print(traceback.format_exc())
        return None


# Should call get_runs
def load_samples_from_runs(run_ids=None, names=None):
    try:
        connection = get_connection()
        db = connection.get_database()
        if run_ids is not None:
            return list(db.runs.find({"_id": {"$in": run_ids}}, {"samples": 1}))
        elif names is not None:
            return list(db.runs.find({"name": {"$in": names}}, {"samples": 1}))
        else:
            return [db.runs.find_one({"$query": {"type": "routine"}, "$orderby": {"_id": -1}})]
    except Exception:
        print(traceback.format_exc())
        return None


def delete_sample_component(s_c_id=None, sample_id=None,
                            s_c_id_list=None, sample_id_list=None):
    """
    DELETE sample component from database. Parameters are AND connected.
    Returns number of deleted entries
    """
    query = []
    if s_c_id is not None:
        query.append({"_id": s_c_id})
    if sample_id is not None:
        query.append({"sample._id": sample_id})
    if s_c_id_list is not None:
        query.append({"_id": {"$in": s_c_id_list}})
    if sample_id_list is not None:
        query.append({"sample._id": {"$in": sample_id_list}})
    try:
        connection = get_connection()
        db = connection.get_database()
        result = db.sample_components.delete_many({"$and": query})
        return result.deleted_count
    except Exception:
        print(traceback.format_exc())
        return None


def delete_sample_from_runs(sample_id=None):
    """
    Delete sample from runs. Returns number of runs this sample was deleted
    from.
    """
    update_count = 0
    try:
        connection = get_connection()
        db = connection.get_database()

        runs = db.runs.find({"samples._id": sample_id})
        for run in runs:
            new_samples = [sample
                            for sample in run["samples"]
                            if sample["_id"] != sample_id]
            run["samples"] = new_samples
            result = db.runs.replace_one({"_id": run["_id"]}, run)
            update_count += result.modified_count
        return update_count
    except Exception:
        print(traceback.format_exc())
        return None


def delete_sample(sample_id):
    try:
        connection = get_connection()
        db = connection.get_database()

        result = db.samples.delete_one({"_id": sample_id})
        return result.deleted_count
    except Exception:
        print(traceback.format_exc())
        return None

# GridFS filehandling

def save_file_to_db(sample_component_id, file_path):
    """
    Will raise an error if file doesn't exist
    """
    connection = get_connection()
    db = connection.get_database()
    fs = gridfs.GridFS(db)

    # check if file is there
    existing = fs.find_one({
        "sample_component_id": sample_component_id,
        "full_path": file_path
    })
    if existing:
        print(("WARNING: File {} already exists in".format(file_path),
        " the db for this component,",
        " it was overwritten by the new file."), file=sys.stderr)
        fs.delete(existing._id)
    
    db_sample_component = next(iter(get_sample_components(sample_component_ids=[sample_component_id])), None)

    mimetype = magic.from_file(file_path, mime=True)

    with open(file_path, 'rb') as file_handle:
        file_id = fs.put(file_handle,
                        sample_component_id=sample_component_id,
                        sample_id=db_sample_component["sample"]["_id"],
                        component_id=db_sample_component["component"]["_id"],
                        full_path=file_path,
                        filename=os.path.basename(file_path),
                        mimetype=mimetype)
    return file_id



def load_file_from_db(file_id, save_to_path=None, subpath=False):

    connection = get_connection()
    db = connection.get_database()
    fs = gridfs.GridFS(db)

    fobj = fs.get(file_id)

    if save_to_path is None:
        if subpath:
            save_to_path = fobj.full_path
        else:
            save_to_path = fobj.filename
    elif os.path.isdir(save_to_path):
        if subpath:
            save_to_path = os.path.join(save_to_path, fobj.full_path)
        else:
            save_to_path = os.path.join(save_to_path, fobj.filename)
        

    if os.path.isfile(save_to_path):
        raise FileExistsError
    
    dirname = os.path.dirname(save_to_path)
    if not os.path.exists(dirname):
        os.makedirs(dirname)


    with open(save_to_path, 'wb') as file_handle:


        file_handle.write(fobj.read())
    return file_id

def find_files(sample_component_id):
    connection = get_connection()
    db = connection.get_database()
    fs = gridfs.GridFS(db)
    return list(fs.find({"sample_component_id":sample_component_id}))
