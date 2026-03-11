---
description: "Use when creating, editing or debugging Tutor plugin code: plugin.py, hooks, patches, templates Mako/Jinja2, SCSS, MFE branding, i18n pt_BR, configurações do Open edX. Cobre convenções do projeto, padrões de config, ciclo de release e checklist para novos MFEs."
applyTo: "ufmtemredebranding/**"
---

# Tutor Plugin — UFMT em Rede Branding

## Contexto do Projeto

Plugin Tutor (`tutor.plugin.v1`) de branding para o UFMT em Rede, baseado no tema Indigo do Open edX.

| Item             | Valor                 |
| ---------------- | --------------------- |
| Python           | >= 3.8                |
| Tutor            | `>= 21.0.0, < 22.0.0` |
| Open edX release | Quince (`17.x.x`)     |
| Locale principal | `pt_BR`               |
| Design system    | Paragon + Sass        |

---

## Convenções de Configuração

- Todas as chaves de configuração do plugin **devem usar o prefixo `UFMT_EM_REDE_`**.
- Declare novos defaults no dict `config["defaults"]` sem o prefixo — o prefixo é aplicado automaticamente via `hooks.Filters.CONFIG_DEFAULTS.add_items`.
- Nunca use `config["overrides"]` para sobrescrever config do core Tutor sem justificativa explícita.

```python
# Correto
config = {
    "defaults": {
        "MY_NEW_SETTING": "value",  # será UFMT_EM_REDE_MY_NEW_SETTING
    }
}

# Errado — jamais adicione o prefixo dentro do dict
config = {
    "defaults": {
        "UFMT_EM_REDE_MY_NEW_SETTING": "value",  # duplica o prefixo
    }
}
```

---

## Patches MFE

- Patches de instalação de pacotes npm seguem o padrão: `mfe-dockerfile-post-npm-install-{nome_do_mfe}`.
- Ao adicionar suporte a um novo MFE, siga este checklist obrigatório:
  1. Adicionar o patch em `hooks.Filters.ENV_PATCHES.add_items` no `plugin.py`
  2. Criar o arquivo de i18n em `templates/mfe/i18n/{nome_do_mfe}/pt_BR.json`
  3. Verificar se o MFE precisa de `@edx/brand`, header e/ou footer customizados

```python
# Template padrão para novo MFE com header + footer
(
    "mfe-dockerfile-post-npm-install-{nome_do_mfe}",
    """
RUN npm install '@edx/brand@git+https://github.com/ejklock/brand-openedx-indigo.git#ufmtemrede/quince'
RUN npm install '@edx/frontend-component-header@npm:@klocktecnologia/indigo-frontend-component-header@1.1.3'
RUN npm install '@edx/frontend-component-footer@npm:@edly-io/indigo-frontend-component-footer@^1.0.0'
""",
),
```

---

## Templates

### Templates Mako (LMS/CMS Django)

- Todo arquivo Mako **deve iniciar** com `## mako` na primeira linha.
- Use `<%page expression_filter="h"/>` em páginas que renderizam conteúdo do usuário (proteção XSS).
- Estrutura de diretório: `templates/ufmtemrede/lms/templates/` espelha a estrutura do LMS.

### Templates Jinja2 (Tutor env)

- Arquivos `.json` e `.po` são tratados como **binários** — não são renderizados pelo Jinja2.
  - Isso é controlado por `CustomRenderer.IGNORE_TEMPLATE_RENDER_EXTENSIONS`.
  - Não use variáveis Jinja2 `{{ }}` em arquivos `.json` ou `.po`.

### SCSS Partials

- Partials em subdiretórios `partials/` **não são renderizados automaticamente** pelo Tutor.
- Sempre registrar explicitamente via `ENV_PATTERNS_INCLUDE`:

```python
hooks.Filters.ENV_PATTERNS_INCLUDE.add_item(r"ufmtemrede/lms/static/sass/partials/lms/theme/")
hooks.Filters.ENV_PATTERNS_INCLUDE.add_item(r"ufmtemrede/cms/static/sass/partials/cms/theme/")
```

---

## Init Tasks

- Init tasks são carregadas de **arquivos**, nunca inline no `plugin.py`.
- Localização: `templates/tasks/{service}/init`
- Usar a função `add_init_tasks(location)` já existente — não reescreva a lógica.

```python
add_init_tasks("lms")     # templates/tasks/lms/init
add_init_tasks("mysql")   # templates/tasks/mysql/init
```

---

## Targets de Template

Mapeamento source → destino no ambiente Tutor:

| Source (relativo ao template root) | Destino Tutor           |
| ---------------------------------- | ----------------------- |
| `ufmtemrede/`                      | `build/openedx/themes`  |
| `brand-openedx/`                   | `plugins/mfe/build/mfe` |
| `local/`                           | `env/local`             |
| `openedx/locale`                   | `build`                 |
| `mfe/i18n`                         | `plugins/mfe/build`     |

---

## Atualização de Release Open edX

Ao migrar para um novo release (ex: Quince → Redwood):

1. Atualizar `__version__` em `__about__.py` (ex: `17.0.0` → `18.0.0`)
2. Atualizar `install_requires` em `setup.py` para o range da nova versão Tutor
3. Atualizar a branch do `brand-openedx-indigo` nos patches MFE (ex: `#ufmtemrede/quince` → `#ufmtemrede/redwood`)
4. Verificar compatibilidade das versões fixadas: `indigo-frontend-component-header` e `indigo-frontend-component-footer`
5. Testar `tutor local do init` após rebuild

---

## Segurança

- Nunca exponha senhas ou credenciais hardcoded fora de `config["defaults"]` (valores default são sobrescritos em produção via `tutor config save`).
- Os valores `EXTERNAL_MYSQL_PASSWORD` em defaults são **placeholders** — devem ser alterados em produção.
- Em templates Mako, sempre use `expression_filter="h"` para conteúdo dinâmico do usuário.

---

## Estrutura de Arquivos do Plugin

```
ufmtemredebranding/
├── __about__.py          # versão do plugin (alinhar ao release Open edX)
├── plugin.py             # ponto central: config, hooks, patches, targets
├── custom_renderer.py    # extensão do Renderer para ignorar .json e .po
├── jinja_custom_environment.py  # ambiente Jinja2 customizado
├── patches/              # patches nomeados exatamente pelo hook Tutor
└── templates/
    ├── brand-openedx/    # pacote npm @edx/brand customizado
    ├── local/            # docker-compose overrides
    ├── mfe/i18n/         # traduções pt_BR por MFE
    ├── openedx/locale/   # .po files do Django (LMS/CMS)
    ├── tasks/            # scripts de init por serviço
    └── ufmtemrede/       # tema LMS/CMS (templates Mako + SCSS)
```
