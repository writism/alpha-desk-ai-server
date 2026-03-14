# Command: /commit

## 목적

현재 변경된 파일을 분석하여 커밋 메시지를 생성하고 커밋을 수행한다.

CLAUDE.md의 아키텍처 규칙을 반영하여 커밋 메시지를 생성한다.

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
4. 커밋 메시지 초안을 사용자에게 보여준다
5. 사용자 승인 후 `git add`와 `git commit`을 실행한다
6. 커밋 완료 후 `git status`로 결과를 확인한다

---

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

변경된 도메인 또는 모듈 이름을 사용한다

예: `stock_normalizer`, `stock_collector`, `watchlist`, `infrastructure`

---

## MUST 규칙

- 커밋 메시지는 사용자 승인 후에만 실행한다
- `main` 브랜치에 직접 커밋하지 않는다. `main` 브랜치인 경우 경고를 출력한다
- 비즈니스 로직 변경이 포함된 경우 CLAUDE.md 아키텍처 규칙 위반 여부를 확인한다

ARGUMENTS: $ARGUMENTS
