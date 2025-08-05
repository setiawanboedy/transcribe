import jwt
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NTQ0NjA0MjAsImlhdCI6MTc1NDM3NDAyMCwic3ViIjoxfQ.lHWOu8AoLSgLvbf0PoGNOIS-PxHeHpbPBJOJ09plMfE"
jwt.decode(token, "transcript-secret-key", algorithms=["HS256"])