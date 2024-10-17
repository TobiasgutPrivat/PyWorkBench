## DataStorage
Mapping from objects to NoSql-Documents (Proxy) seamless data storage.
Specific save/load -handling possible

### Database
**MongoDB**
currently: local -> mongodb://localhost:27017/, with mongoDB compass
simple, popular, fast (no Vector indexing)

## Serialization
**Dill**, because provides very complete serialization for all types, and recreates instances. (Performance a bit worse than pickle)