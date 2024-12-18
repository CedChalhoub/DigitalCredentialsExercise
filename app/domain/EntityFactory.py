from app.domain.Entity import Entity


class EntityFactory:
    def create(self, entityType: str) -> Entity:
        match entityType:
            case "Federal Government":
                return