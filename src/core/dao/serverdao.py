from typing import Union
from sqlalchemy.orm import Query
from core.model import DBSession
from core.model.server import Server
from core.utils import whoami, class_name


class ServerDao:
    def __init__(self):
        pass

    def insert(self, new_server: Union[Server, list[Server], tuple[Server], set[Server]]) -> Union[tuple, None]:
        """
        Inserts one or several new Server instances into the database, if they don't exist that is.
        ### Params
        * `new_server: Server | list | tuple | set` - The server instance(s) to insert.
        ### Returns
        * `successes: int, failures: int` - Tuple
        * `None` if no new instances to add
        """
        if not new_server:
            return None

        if isinstance(new_server, Server):
            exists = bool(self.find('id', new_server.server_id))
            if exists:
                return None
            else:
                try:
                    DBSession.add(new_server)
                    return 1, 0
                except Exception as e:
                    print(f"Exception thrown at {class_name(self)}.{whoami()}:\n{e}")
                    return 0, 1
        else:
            successes = 0
            failures = 0
            for servo in new_server:
                if not isinstance(servo, Server) or bool(self.find('id', servo.server_id)):
                    continue
                try:
                    DBSession.add(servo)
                    successes += 1
                except Exception as e:
                    print(f"Exception thrown at {class_name(self)}.{whoami()}:\n{e}")
                    failures += 1
            return successes, failures

    def find(self, by: str, terms: Union[int, str]) -> Union[Server, list, None]:
        """
        Finds one or multiple Servers. Returns `None` if no results are found.
        ### Params
        * `by: 'id' | 'name'` - Decides whether to search by discord ID or name.
        * `terms: int | str` - Query terms. Must be an integer if `"by == 'id'"` or a string if `"by == 'name'"`.
        ### Returns
        * `Server` if `by == 'id'`
        * `list[Server]` if `by == 'name'`
        * `None` if no matches were found for either
        """
        if by not in ('id', 'name'):
            raise SyntaxError("incorrect parameter 'by' passed")
        elif terms is None:
            return None

        q: Query = DBSession.query(Server)
        if by == 'id':
            q = q.filter(Server.server_id == int(terms)).first()
        else:
            q = q.filter(Server.server_name.ilike(str(terms))).all()
            if not q:
                q = None

        return q

    def update(self, server: Union[Server, list, tuple, set]) -> Union[tuple, None]:
        """
        Updates one or multiple servers, as long as they exist.
        ### Params
        * `server: Server | list | tuple | set` - The server(s) to update.
        ### Returns
        * `successes: int, failures: int` - Tuple
        * `None` if no instances to update
        """
        if not server:
            return None

        if isinstance(server, Server):
            cur_servo = self.find('id', server.server_id)
            if cur_servo is None:
                return None
            else:
                try:
                    cur_servo.import_server(server)
                    return 1, 0
                except Exception as e:
                    print(f"Exception thrown at {class_name(self)}.{whoami()}:\n{e}")
                    return 0, 1
        else:
            successes = 0
            failures = 0
            for servo in server:
                if not isinstance(servo, Server):
                    continue
                try:
                    cur_servo = self.find('id', servo.server_id)
                    if cur_servo is None:
                        failures += 1
                        continue
                    cur_servo.import_server(servo)
                    successes += 1
                except Exception as e:
                    print(f"Exception thrown at {class_name(self)}.{whoami()}:\n{e}")
                    failures += 1
            return successes, failures

    def delete(self, server: Union[Server, int, list, tuple, set]) -> Union[tuple, None]:
        """
        Deletes one or multiple servers, provided they exist.
        ### Params
        * `server: Server | int | list | tuple | set` - The Server(s) or server ID(s) to delete.
        ### Returns
        * `successes: int, failures: int` - Tuple
        * `None` if no instances to delete
        """

        if not server:
            return None
        if isinstance(server, Server) or isinstance(server, int):
            del_server = self.find('id', server if isinstance(server, int) else server.id)
            if del_server is None:
                return None
            else:
                try:
                    DBSession.delete(del_server)
                    return 1, 0
                except Exception as e:
                    print(f"Exception thrown at {class_name(self)}.{whoami()}:\n{e}")
                    return 0, 1
        else:
            successes = 0
            failures = 0
            for servo in server:
                if not isinstance(servo, Server) or isinstance(servo, int):
                    continue
                del_server = self.find('id', servo if isinstance(servo, int) else servo.id)
                if del_server is None:
                    failures += 1
                else:
                    try:
                        DBSession.delete(del_server)
                        successes += 1
                    except Exception as e:
                        print(f"Exception thrown at {class_name(self)}.{whoami()}:\n{e}")
                        failures += 1
            return successes, failures
