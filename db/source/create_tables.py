#!/usr/bin/env python2.7

import os
from boto.dynamodb2.table import Table
from boto.dynamodb2.layer1 import DynamoDBConnection
from boto.dynamodb2.fields import HashKey, GlobalAllIndex

def init_connection():
    host = "localhost"
    port = 8040

    return DynamoDBConnection(
        aws_access_key_id='foo',
        aws_secret_access_key='bar',
        host=host,
        port=port,
        is_secure=False)


def create_tables():
    conn = init_connection()

    tables = conn.list_tables()["TableNames"]
    for name in tables:
        Table(name, connection=conn).delete()


    Table.create("DelegateIt_Customers",
        schema=[
            HashKey("uuid"),
        ],
        global_indexes=[
            GlobalAllIndex("phone_number-index", parts=[
                HashKey("phone_number"),
            ]),
        ],
        connection=conn
    )
    Table.create("DelegateIt_Delegators",
        schema=[
            HashKey("uuid"),
        ],
        global_indexes=[
            GlobalAllIndex("phone_number-index", parts=[
                HashKey("phone_number"),
            ]),
            GlobalAllIndex("email-index", parts=[
                HashKey("email"),
            ]),
        ],
        connection=conn
    )
    Table.create("DelegateIt_Transactions",
        schema=[
            HashKey("uuid"),
        ],
        global_indexes=[
            GlobalAllIndex("status-index", parts=[
                HashKey("status"),
            ]),
        ],
        connection=conn
    )
    Table.create("DelegateIt_Handlers", schema=[HashKey("transaction_uuid")], connection=conn)

if __name__ == "__main__":
    create_tables()
