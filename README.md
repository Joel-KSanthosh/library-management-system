# Library-Management-System
This is a Fastapi project which manages the library system 

## Changes to make
- Use SQLAlchemy instead of SQLModel, full change needed -> Done
- Update so that migrations can be done from fastapi itself. i.e; fastapi -> alembic -> Done
- Need to use async session properly -> Almost Done
- Verify the model validations , before insertions