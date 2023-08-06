import psycopg2


class Database:
    """
    Classe per la connessione un database SQL e le successive interrogazioni verso lo stesso
    """

    __database_cursor = None            # cursore del database da utilizzare per le query


    def __init__(self, host, port, database, user, password, autocommit=True):
        """
        Inizializza la connessione con il database SQL
        :param host:            indirizzo dell'host del database
        :param port:            porta di connessione del database
        :param database:        nome del database al quale ci si vuole connettere
        :param user:            utente con cui connettersi e autenticarsi
        :param password:        password dell'utente specificato
        :param autocommit:      passa alla modalità autocommit, ogni comando ha effetto immediatamente
        :throw RuntimeError:    se la connessione non ha avuto successo             
        """
        try:
            # apro la connessione ed ottengo il cursore
            db_connection = psycopg2.connect(port=port, host=host, dbname=database, user=user, password=password)
            db_connection.set_session(autocommit=autocommit)
            self.__database_cursor = db_connection.cursor()
        except (Exception, psycopg2.Error) as error:
            # nel caso ci siano problemi con la connessione sollevo un'eccezione
            raise RuntimeError('Exception connetcting to Database: {}:{}'.format(host, port)) from error

    def query_first(self, query, params=None):
        """
        Esegue la query <query> con parametri <params> sul database e ritorna al massimo una entry
        I placeholders nella query hanno formato %(placeholder)s
        :param query:           stringa contenente la query da eseguire
        :param params:          placeholder da sostituire
        :throw RuntimeError:    se qualcosa è andato storto nella query
        :return:                risultato della query, massimo una entry
        """
        try:
            params = {} if params is None else params
            # eseguo la query e restituisco solo il primo risultato
            self.__database_cursor.execute(query, params)
            return self.__database_cursor.fetchone()
        except Exception as e:
            # qualcosa è andato storto nella query, sollevo un'eccezione
            raise RuntimeError('Exception while executing query "{}" with params "{}"'.format(query, params)) from e

    def query_all(self, query, params=None):
        """
        Esegue la query <query> con parametri <params> sul database e ritorna tutte le entries
        I placeholders nella query hanno formato %(placeholder)s
        :param query:           stringa contenente la query da eseguire
        :param params:          placeholder da sostituire
        :throw RuntimeError:    se qualcosa è andato storto nella query
        :return:                risultato della query, tutte le entries
        """

        try:
            params = {} if params is None else params
            # eseguo la query e restituisco tutti i risultati
            self.__database_cursor.execute(query, params)
            return self.__database_cursor.fetchall()
        except Exception as e:
            # qualcosa è andato storto nella query, sollevo un'eccezione
            raise RuntimeError('Exception while executing query "{}" with params "{}"'.format(query, params)) from e

    def query_no_result(self, query, params=None):
        """
        Esegue la query <query> con parametri <params> sul database senza ottenere risultati
        I placeholders nella query hanno formato %(placeholder)s
        :param query:           stringa contenente la query da eseguire
        :param params:          placeholder da sostituire
        :throw RuntimeError:    se qualcosa è andato storto nella query
        """
        try:
            params = {} if params is None else params
            self.__database_cursor.execute(query, params)
        except Exception as e:
            # qualcosa è andato storto nella query, sollevo un'eccezione
            raise RuntimeError('Exception while executing query "{}" with params "{}"'.format(query, params)) from e
