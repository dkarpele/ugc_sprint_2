print( "Creating mongo db...");
db.createUser(
        {
            user: process.env.MONGO_INITDB_ROOT_USERNAME,
            pwd:  process.env.MONGO_INITDB_ROOT_PASSWORD,
            roles: [
                {
                    role: "readWrite",
                    db: process.env.MONGO_INITDB_DATABASE
                }
            ]
        }
);


// db.createCollection($MONGO_INITDB_DATABASE.likes)
//echo "db.createCollection(\"$MONGO_INITDB_DATABASE.reviews\")" | \
//mongosh mongodb://"$MONGO_INITDB_ROOT_USERNAME":"$MONGO_INITDB_ROOT_PASSWORD"@localhost:27017/
//
//echo "db.createCollection(\"$MONGO_INITDB_DATABASE.bookmarks\")" | \
//mongosh mongodb://"$MONGO_INITDB_ROOT_USERNAME":"$MONGO_INITDB_ROOT_PASSWORD"@localhost:27017/
//
//echo "Collections have been created."
//
//echo "db.bookmarks.createIndex( { \"user_id\": 1, \"movie_id\": 1 } , { unique: true } )" | \
//mongosh mongodb://"$MONGO_INITDB_ROOT_USERNAME":"$MONGO_INITDB_ROOT_PASSWORD"@localhost:27017/
