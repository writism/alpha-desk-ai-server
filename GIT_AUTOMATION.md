# Git Commit & PR 자동화 방안

## 1. 현재 환경 상태

### Git 설정

| 항목 | 값 |
|---|---|
| 현재 브랜치 | `main` |
| Remote | `origin` → `https://github.com/writism/alpha-desk-ai-server.git` |
| 원격 브랜치 | `origin/main`, `origin/develop` |
| 작업 브랜치 | `feature/r2-normalizer` (로컬 미생성 상태) |

**현재 변경 사항 (미커밋)**

- 수정됨: `.claude/settings.local.json`, `CLAUDE.md`, `app/infrastructure/config/settings.py`, `main.py`
- 미추적: `PROJECT_ANALYSIS.md`, `app/domains/`

### gh CLI 설치 상태

- **gh CLI: 미설치** (`command not found`)
- Homebrew는 설치되어 있으므로 `brew install gh`로 즉시 설치 가능

### Claude Code 커스텀 커맨드 현황

`.claude/commands/` 디렉토리에 다음 커맨드가 존재한다:

| 커맨드 | 파일 | 설명 |
|---|---|---|
| `/backlog` | `backlog.md` | Behavior Backlog 생성 |
| `/implement` | `implement.md` | Backlog 기반 코드 구현 |

**결론: `/commit`, `/pr` 커스텀 커맨드는 현재 존재하지 않는다.**

`.claude/skills/` 디렉토리에는 `BEHAVIOR_BACKLOG_GENERATOR.md` 스킬만 존재한다.

### Git Hooks 상태

`.git/hooks/`에는 샘플 파일(`.sample`)만 존재하며, 활성화된 훅은 없다.

---

## 2. 자동화 옵션 비교

### 옵션 A — Claude Code 커스텀 커맨드 (`/commit`, `/pr`)

Claude Code의 `.claude/commands/` 디렉토리에 마크다운 파일로 커맨드를 정의한다. Claude Code 세션 내에서 `/commit`, `/pr`을 입력하면 정의된 규칙에 따라 자동으로 커밋 메시지 생성 및 PR 생성 절차를 수행한다.

**장점**

- 프로젝트 컨텍스트(변경 파일, diff)를 Claude가 직접 읽어 커밋 메시지 품질이 높다
- 이 프로젝트의 CLAUDE.md 아키텍처 규칙을 이해한 상태에서 메시지를 생성한다
- 팀원이 동일한 `.claude/commands/` 파일을 공유하면 일관된 커밋 스타일을 유지한다
- gh CLI가 설치되어 있으면 PR 생성까지 한 번에 처리할 수 있다
- 추가 도구 학습 비용이 없다 (이미 Claude Code를 사용 중이므로)

**단점**

- Claude Code 세션을 실행 중일 때만 사용 가능하다
- 내부적으로 gh CLI를 호출하므로 gh CLI 설치가 필요하다

---

### 옵션 B — gh CLI 직접 사용

터미널에서 직접 git과 gh CLI 명령어를 조합한다.

```bash
git add <files>
git commit -m "feat: ..."
git push origin feature/r2-normalizer
gh pr create --title "..." --body "..."
```

**장점**

- 의존성이 단순하다 (git + gh CLI만 필요)
- 스크립트(`.sh`)로 래핑하면 반복 작업을 자동화할 수 있다
- CI/CD 파이프라인과 통합하기 쉽다

**단점**

- 커밋 메시지를 사람이 직접 작성해야 한다
- PR 본문을 매번 수동으로 작성해야 한다
- 팀원마다 커밋 스타일이 달라질 수 있다

---

### 옵션 C — Git Hook 활용 (`prepare-commit-msg`, `pre-push`)

`.git/hooks/` 또는 `.githooks/` 디렉토리에 쉘 스크립트를 작성하여 커밋 메시지 템플릿 주입, pre-push 시 브랜치 보호 등을 자동화한다.

**장점**

- git 자체 기능이므로 별도 도구 없이 동작한다
- `prepare-commit-msg` 훅으로 커밋 메시지 템플릿을 자동 삽입할 수 있다
- `.githooks/` 디렉토리에 두고 git 설정으로 공유하면 팀 전체에 적용 가능하다

**단점**

- 커밋 메시지 내용 자동화는 어렵다 (템플릿 수준에 머문다)
- PR 생성은 불가능하다 (gh CLI를 훅 내부에서 호출해야 한다)
- 훅 활성화를 각 개발자가 직접 설정해야 한다 (`git config core.hooksPath .githooks`)

---

### 옵션 비교 요약

| 기준 | Claude Code 커맨드 | gh CLI 직접 사용 | Git Hook |
|---|---|---|---|
| 커밋 메시지 품질 | 높음 (AI 생성) | 낮음 (수동) | 중간 (템플릿) |
| PR 생성 자동화 | 가능 | 가능 | 어려움 |
| 설치 필요 도구 | gh CLI | gh CLI | 없음 |
| 팀 공유 용이성 | 높음 | 중간 | 중간 |
| Claude Code 없이 사용 | 불가 | 가능 | 가능 |
| 아키텍처 규칙 반영 | 자동 | 수동 | 불가 |

---

## 3. 추천 방안

**Claude Code 커스텀 커맨드 (`/commit` + `/pr`) + gh CLI 조합**을 추천한다.

### 추천 이유

1. **이미 Claude Code를 주 개발 도구로 사용 중이다.** `/backlog`, `/implement` 커맨드가 이미 정착된 워크플로우 위에 `/commit`, `/pr`을 추가하면 개발-커밋-PR의 전 과정이 Claude Code 안에서 완결된다.

2. **CLAUDE.md 아키텍처 규칙을 커밋에 반영할 수 있다.** Claude는 변경된 파일이 Domain Layer인지 Application Layer인지 판단하여 커밋 메시지에 적절한 컨텍스트를 포함할 수 있다.

3. **커밋 메시지 품질이 가장 높다.** git diff를 직접 분석하여 "what"이 아닌 "why" 중심의 커밋 메시지를 생성한다.

4. **gh CLI는 Homebrew로 즉시 설치 가능하다.** 환경 구성 비용이 낮다.

5. **`.claude/commands/` 파일은 git으로 공유된다.** 팀원이 동일한 커밋/PR 스타일을 유지할 수 있다.

---

## 4. 구현 방법

### Step 1 — gh CLI 설치 및 인증

```bash
brew install gh
gh auth login
```

`gh auth login` 실행 후 다음을 선택한다:

- 플랫폼: `GitHub.com`
- 프로토콜: `HTTPS`
- 인증 방법: `Login with a web browser` (브라우저에서 코드 입력)

인증 확인:

```bash
gh auth status
```

---

### Step 2 — `/commit` 커스텀 커맨드 생성

파일 경로: `/Users/sulee/dev/codelab/alpha-desk-ai-server/.claude/commands/commit.md`

```markdown
# Command: /commit

## 목적

현재 변경된 파일을 분석하여 커밋 메시지를 생성하고 커밋을 수행한다.

이 Command는 CLAUDE.md의 아키텍처 규칙을 반영하여 커밋 메시지를 생성한다.

---

## 사용 방법

```
/commit
```

또는

```
/commit <추가 컨텍스트>
```

---

## 동작 규칙

1. `git status`로 변경된 파일 목록을 확인한다
2. `git diff`로 실제 변경 내용을 분석한다
3. 변경 레이어를 파악한다 (Domain / Application / Adapter / Infrastructure)
4. 다음 형식으로 커밋 메시지를 생성한다

## 커밋 메시지 형식

```
<type>(<scope>): <subject>

<body>

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
```

### type 규칙

- `feat`: 새 기능 추가
- `fix`: 버그 수정
- `refactor`: 리팩토링 (기능 변경 없음)
- `chore`: 설정, 의존성 변경
- `docs`: 문서 변경

### scope 규칙

- 변경된 도메인 이름 또는 레이어 이름을 사용한다
- 예: `post`, `auth`, `infrastructure`, `config`

## 실행 절차

1. 커밋 메시지 초안을 사용자에게 보여준다
2. 사용자 승인 후 `git add`와 `git commit`을 실행한다
3. 커밋 완료 후 `git status`로 결과를 확인한다

## MUST 규칙

커밋 메시지에 비즈니스 로직 변경이 포함되어 있으면
CLAUDE.md의 아키텍처 규칙(Domain/Application/Adapter 분리)을 위반했는지 확인한다.
```

---

### Step 3 — `/pr` 커스텀 커맨드 생성

파일 경로: `/Users/sulee/dev/codelab/alpha-desk-ai-server/.claude/commands/pr.md`

```markdown
# Command: /pr

## 목적

현재 브랜치의 커밋 이력을 분석하여 GitHub Pull Request를 생성한다.

---

## 사용 방법

```
/pr
```

또는

```
/pr <base-branch>
```

base-branch를 생략하면 기본값은 `develop`이다.

---

## 동작 규칙

1. 현재 브랜치 이름을 확인한다
2. `git log <base>...HEAD`로 커밋 이력을 분석한다
3. `git diff <base>...HEAD`로 전체 변경 내용을 파악한다
4. PR 제목과 본문을 생성한다
5. `git push origin <branch>`로 원격에 푸시한다
6. `gh pr create`로 PR을 생성한다

## PR 본문 형식

```
## Summary
- <변경 사항 요약 bullet point>

## Changes
- <레이어별 변경 파일 목록>

## Test plan
- [ ] <검증 항목>

## Architecture Check
- [ ] Domain Layer가 순수 Python인가
- [ ] ORM이 Domain Entity와 분리되어 있는가
- [ ] DTO가 Domain Entity와 분리되어 있는가

🤖 Generated with Claude Code
```

## MUST 규칙

- PR 제목은 70자 이하로 작성한다
- base 브랜치가 `main`인 경우 사용자에게 한 번 더 확인을 요청한다
```

---

### Step 4 — 작업 브랜치 생성

```bash
git checkout -b feature/r2-normalizer
git push -u origin feature/r2-normalizer
```

---

### Step 5 — .claude/commands/ 파일을 git에 추가

```bash
git add .claude/commands/commit.md .claude/commands/pr.md
git commit -m "chore(.claude): add /commit and /pr custom commands"
git push origin feature/r2-normalizer
```

---

## 5. 사용 예시

### 시나리오: `feature/r2-normalizer` 브랜치에서 구현 완료 후 PR 생성

**Step 1 — 구현 완료 후 Claude Code에서 커밋 실행**

```
/implement 인증되지 않은 사용자가 게시물 리스트를 조회한다
```

구현이 완료되면:

```
/commit
```

Claude가 다음을 수행한다:
1. `git status`, `git diff` 분석
2. 커밋 메시지 초안 제시
3. 사용자 승인 후 커밋 실행

예시 커밋 메시지:

```
feat(post): add unauthenticated post list retrieval

Implement GET /posts endpoint for unauthenticated access.
- PostListUseCase in application layer
- PostQueryRepository port with SQLAlchemy adapter
- PostListResponse DTO separated from domain entity

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
```

---

**Step 2 — PR 생성**

```
/pr develop
```

Claude가 다음을 수행한다:
1. `git log develop...HEAD` 분석
2. PR 제목 및 본문 생성 후 미리보기 제시
3. 사용자 승인 후 `git push` + `gh pr create` 실행

예시 PR 제목:

```
feat(post): add unauthenticated post list API
```

예시 PR 본문:

```markdown
## Summary
- 인증되지 않은 사용자의 게시물 리스트 조회 API 추가
- Hexagonal Architecture 규칙에 따른 레이어 분리 적용

## Changes
- `app/domains/post/adapter/inbound/api/post_router.py`
- `app/domains/post/application/usecase/get_post_list_usecase.py`
- `app/domains/post/application/response/post_list_response.py`
- `app/domains/post/domain/entity/post.py`

## Test plan
- [ ] GET /posts 200 응답 확인
- [ ] 빈 리스트 반환 확인
- [ ] 페이지네이션 파라미터 동작 확인

## Architecture Check
- [x] Domain Layer가 순수 Python인가
- [x] ORM이 Domain Entity와 분리되어 있는가
- [x] DTO가 Domain Entity와 분리되어 있는가

🤖 Generated with Claude Code
```

---

### 빠른 참조 — 커맨드 체인

```
# 1. 구현
/implement <Backlog Title>

# 2. 커밋
/commit

# 3. PR 생성 (base: develop)
/pr develop
```

---

## 참고 — gh CLI 주요 명령어

```bash
# PR 목록 조회
gh pr list

# PR 상태 확인
gh pr status

# PR 웹에서 열기
gh pr view --web

# PR 병합
gh pr merge <pr-number>

# 브랜치 PR 확인
gh pr checks
```
