# Command: /pr

## 목적

현재 브랜치의 커밋 이력을 분석하여 GitHub Pull Request를 생성한다.

gh CLI를 사용하여 PR을 생성한다.

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
4. PR 제목과 본문 초안을 사용자에게 보여준다
5. 사용자 승인 후 `git push origin <branch>`로 원격에 푸시한다
6. `gh pr create`로 PR을 생성한다

---

## PR 본문 형식

```markdown
## Summary
- <변경 사항 요약>

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

---

## MUST 규칙

- PR 제목은 70자 이하로 작성한다
- PR 생성 전 반드시 사용자 승인을 받는다
- base 브랜치가 `main`인 경우 사용자에게 한 번 더 확인을 요청한다

ARGUMENTS: $ARGUMENTS
