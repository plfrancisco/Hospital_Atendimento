# 📊 Modelo Entidade-Relacionamento (MER) - Sistema Hospitalar V2 (Expandido)

```mermaid
erDiagram
    PACIENTE ||--o{ ATENDIMENTO : "possui"
    PACIENTE ||--o{ CONSULTA : "agenda"
    MEDICO ||--o{ CONSULTA : "realiza"
    PACIENTE ||--o{ INTERNACAO : "recebe"
    LEITO ||--o{ INTERNACAO : "aloca"
    ENFERMEIRA ||--o{ ATENDIMENTO : "realiza triagem"
    ENFERMEIRA ||--o{ DIARIO_ENFERMAGEM : "registra"
    INTERNACAO ||--o{ DIARIO_ENFERMAGEM : "possui"

    PACIENTE {
        int id PK
        string nome
        string cpf UK
        string prioridade
    }

    ATENDIMENTO {
        int id PK
        int paciente_id FK
        int medico_id FK
        int enfermeira_id FK
        string status
        datetime data_chegada
        datetime data_triagem
        datetime data_atendimento
        text sintomas
        text sinais_vitais
    }

    MEDICO {
        int id PK
        string nome
        string crm UK
        string especialidade
    }

    ENFERMEIRA {
        int id PK
        string nome
        string coren UK
    }

    CONSULTA {
        int id PK
        int paciente_id FK
        int medico_id FK
        datetime data_hora
        string status
        text observacoes
    }

    LEITO {
        int id PK
        string numero UK
        string tipo
        string status
    }

    INTERNACAO {
        int id PK
        int paciente_id FK
        int leito_id FK
        datetime data_entrada
        datetime data_saida
        text motivo
    }

    DIARIO_ENFERMAGEM {
        int id PK
        int internacao_id FK
        int enfermeira_id FK
        text observacao
        datetime data_registro
    }
```

---
**Nota:** Este diagrama reflete a arquitetura expandida com Gestão Clínica, Rodízio de Enfermagem e Evolução Diária.
