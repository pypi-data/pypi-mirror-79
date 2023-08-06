# UUID-str type

Here resides a UUID-str type for SQLAlchemy. Which stores a UUID-like string in
the database as a UUID when it can and falls back to BINARY(16) or a CHAR(32)
when it can't.

## Rationale

A lot of projects tend to use UUIDs as a unique identifier for entities in
their systems. Also, microservices have gotten quite popular these days. Most
projects try to follow REST-ful API design. Now when talking to another
microservice or our DB. We can end up with some entities with string ID and
some with UUID. This causes inconsistency in a system. Thre are two potential
fixes to this.
1. Make sure that you convert all the ids in JSON-objects that you get from
   downstream services into UUID objects. 
2. Keep everything string.

We prefer the 2nd option reasoning for that includes except when storing it in
DB.
1. Let's start with the argument of simplicity. We believe that both have an
   equal level of simplicity. Both require you to identify and convert UUIDs at
   a particular level. So there is no clear winner with this argument.
2. Next up the ease of implementation, our belief is that 2nd one is far easier
   to implement. Case in point this lib. We don't need anything else. Whereas
   in the first one deterministically determining which ones are UUIDs can not
   be achieved by just a type wrapper, it requires a nested scan or a manual
   selection of each one.
3. We do not do type-specific operations. So annotating this data with UUID,
   does not give us any benefit.
4. Ease in dealing with strings. e.g. You can give simpler names in your tests.

## Usage

```python
class User(Base):
    __tablename__ = "user"
    id = Column(UUIDType, primary_key=True)


user_id = str(uuid4())
user = User(id=user_id)
session.add(user)
session.commit()

user_db = session.query(User).filter(User.id == user_id).one()
assert isinstance(user_db.id, str)
```
