#!/bin/sh

echo "Creating mongo db..."
echo "use $MONGO_INITDB_DATABASE" | \
mongosh mongodb://"$MONGO_INITDB_ROOT_USERNAME":"$MONGO_INITDB_ROOT_PASSWORD"@localhost:27017/admin
echo "Mongo db created."

echo "db.createCollection(\"$MONGO_INITDB_DATABASE.likes\")" | \
mongosh mongodb://"$MONGO_INITDB_ROOT_USERNAME":"$MONGO_INITDB_ROOT_PASSWORD"@localhost:27017/admin

echo "db.createCollection(\"$MONGO_INITDB_DATABASE.reviews\")" | \
mongosh mongodb://"$MONGO_INITDB_ROOT_USERNAME":"$MONGO_INITDB_ROOT_PASSWORD"@localhost:27017/admin

echo "db.createCollection(\"$MONGO_INITDB_DATABASE.bookmarks\")" | \
mongosh mongodb://"$MONGO_INITDB_ROOT_USERNAME":"$MONGO_INITDB_ROOT_PASSWORD"@localhost:27017/admin

echo "Collections have been created."