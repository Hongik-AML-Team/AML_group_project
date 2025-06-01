--- Detailed Failure Cases (display_dataframe_to_user not available) ---
                                                            입력 설명 (src)                                                                            예상 정답 (tgt)                                                                                                                                                               모델 출력 (pred)                                                                             오류 메시지                 오류 유형
0                                       Make dictionary from list with python                                          dict(x[i:i + 2] for i in range(0, len(x), 2))                                                                                                                                       dict([(k, v) for k, v in zip(keys, values)]                                            '(' was never closed (<string>, line 1)                    기타
1                        Find a value within nested json dictionary in python                                list(data['A']['B'].values())[0]['maindata'][0]['Info']                                                                                                                      try:\n    return next(iter(d.values()) if next(d) else None)                            expected 'except' or 'finally' block (<string>, line 2)                    기타
2                                Converting lists of tuples to strings Python                                               """ """.join([('%d@%d' % t) for t in l])                                                                                                                               """""".join([item[0] for item in L] for item in L)]                                                   unmatched ']' (<string>, line 1)                    기타
3                                Converting lists of tuples to strings Python                                    """ """.join([('%d@%d' % (t[0], t[1])) for t in l])                                                                                                                               """""".join([item[0] for item in L] for item in L)]                                                   unmatched ']' (<string>, line 1)                    기타
4                                     printing tab-separated values of a list                                                       print('\t'.join(map(str, list)))                                                                                                                                    print('\t'.join(map(str, myList)) for myList))                                                   unmatched ')' (<string>, line 1)                    기타
5                             finding n largest differences between two lists                   heapq.nlargest(10, range(len(l1)), key=lambda i: abs(l1[i] - l2[i]))                                                                                                                                       max(len(a) - len(b)) for a, b in zip(a, b))                                                   unmatched ')' (<string>, line 1)                    기타
6            How do I convert tuple of tuples to list in one line (pythonic)?  from functools import reduce\nreduce(lambda a, b: a + b, (('aa',), ('bb',), ('cc',)))                                                                                                                                                         list(map(list, zip(*t))))                                                   unmatched ')' (<string>, line 1)                    기타
7            How do I convert tuple of tuples to list in one line (pythonic)?                                       map(lambda a: a[0], (('aa',), ('bb',), ('cc',)))                                                                                                                                                         list(map(list, zip(*t))))                                                   unmatched ')' (<string>, line 1)                    기타
8                           Django view returning json without using template                                 return HttpResponse(data, mimetype='application/json')                                                                                                   return HttpResponse(json.dumps(response_data), content_type='application/json')                                       'return' outside function (<string>, line 1)                    기타
9                    Create dictionary from lists of keys and multiple values                                                   dict([('Name', 'Joe'), ('Age', 22)])                                                                                                                                      dict([(k, v) for k, v in zip(keys, values))]  closing parenthesis ')' does not match opening parenthesis '[' (<string>, line 1)                    기타
10                                     How to reverse a dictionary in Python?                                       {i[1]: i[0] for i in list(myDictionary.items())}                                                                                                                                  dict((k, reverse(v) for k, v in list(d.items()))                                                  invalid syntax (<string>, line 1)                 문법 오류
11                              How do I return a 401 Unauthorized in Django?                                        return HttpResponse('Unauthorized', status=401)                                                                                                                                                   return HttpResponse(status=401)                                       'return' outside function (<string>, line 1)                    기타
12                  How do I INSERT INTO t1 (SELECT * FROM t2) in SQLAlchemy?                                   session.execute('INSERT INTO t1 (SELECT * FROM t2)')  cursor.execute('INSERT INTO table VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s                unterminated string literal (detected at line 1) (<string>, line 1)  괄호/따옴표 안 닫힘 (EOF 오류)
13          How to delete all instances of a character in a string in python?                             """""".join([char for char in 'it is icy' if char != 'i'])                                                                                                                                         """""".join(c for c in s if c.isalpha()])  closing parenthesis ']' does not match opening parenthesis '(' (<string>, line 1)                    기타
14          How to delete all instances of a character in a string in python?                                                           re.sub('i', '', 'it is icy')                                                                                                                                         """""".join(c for c in s if c.isalpha()])  closing parenthesis ']' does not match opening parenthesis '(' (<string>, line 1)                    기타
15          How to delete all instances of a character in a string in python?                                                       """it is icy""".replace('i', '')                                                                                                                                         """""".join(c for c in s if c.isalpha()])  closing parenthesis ']' does not match opening parenthesis '(' (<string>, line 1)                    기타
16          How to delete all instances of a character in a string in python?                             """""".join([char for char in 'it is icy' if char != 'i'])                                                                                                                                         """""".join(c for c in s if c.isalpha()])  closing parenthesis ']' does not match opening parenthesis '(' (<string>, line 1)                    기타
17                                  Reading unicode elements into numpy array            arr = numpy.fromiter(codecs.open('new.txt', encoding='utf-8'), dtype='<U2')                     numpy.fromstring('\u0420\u0430\u0430\u0430\u0430\u0430\u0430\u0430\u0430\u0430\u0430\u0430\u0430\u0430\u0430\u0430\u0430\u0430\u0430\u0430\u0430\u0430\u0430\                unterminated string literal (detected at line 1) (<string>, line 1)  괄호/따옴표 안 닫힘 (EOF 오류)
18  Sending post data from angularjs to django as JSON and not as raw content                                                               json.loads(request.body)                                                                                                                                         return HttpResponse(json.dumps(postdata))                                       'return' outside function (<string>, line 1)                    기타

# 모델 컴파일 오류 분석 보고서

## 1. 오류 유형별 통계

| 오류 유형                      |   발생 횟수 |
|:-------------------------------|------------:|
| 기타                           |          16 |
| 괄호/따옴표 안 닫힘 (EOF 오류) |           2 |
| 문법 오류                      |           1 |


## 2. 오류 유형별 상세 예시 및 분석

### 2.1. 기타 (16건)

#### 예시 1

**입력 설명 (src):**
> Make dictionary from list with python

**모델 출력 (pred):**
python
dict([(k, v) for k, v in zip(keys, values)]


**오류 메시지:**
> '(' was never closed (<string>, line 1)

**분석 및 개선 방향:**

- **원인:** 위 범주에 속하지 않는 다양한 오류.
- **개선:** 개별 오류 메시지를 상세히 검토하여 근본 원인을 파악하고, 해당 패턴을 줄일 수 있는 데이터나 모델 개선 방향을 모색해야 합니다.
---

#### 예시 2

**입력 설명 (src):**
> Find a value within nested json dictionary in python

**모델 출력 (pred):**
python
try:
    return next(iter(d.values()) if next(d) else None)


**오류 메시지:**
> expected 'except' or 'finally' block (<string>, line 2)

**분석 및 개선 방향:**

- **원인:** 위 범주에 속하지 않는 다양한 오류.
- **개선:** 개별 오류 메시지를 상세히 검토하여 근본 원인을 파악하고, 해당 패턴을 줄일 수 있는 데이터나 모델 개선 방향을 모색해야 합니다.
---

#### 예시 3

**입력 설명 (src):**
> Converting lists of tuples to strings Python

**모델 출력 (pred):**
python
"""""".join([item[0] for item in L] for item in L)]


**오류 메시지:**
> unmatched ']' (<string>, line 1)

**분석 및 개선 방향:**

- **원인:** 위 범주에 속하지 않는 다양한 오류.
- **개선:** 개별 오류 메시지를 상세히 검토하여 근본 원인을 파악하고, 해당 패턴을 줄일 수 있는 데이터나 모델 개선 방향을 모색해야 합니다.
---

### 2.2. 괄호/따옴표 안 닫힘 (EOF 오류) (2건)

#### 예시 13

**입력 설명 (src):**
> How do I INSERT INTO t1 (SELECT * FROM t2) in SQLAlchemy?

**모델 출력 (pred):**
python
cursor.execute('INSERT INTO table VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s


**오류 메시지:**
> unterminated string literal (detected at line 1) (<string>, line 1)

**분석 및 개선 방향:**

- **원인:** 문장 끝에 괄호나 따옴표가 닫히지 않았거나, 블록이 제대로 끝나지 않음.
- **개선:** 모델 학습 시 일관된 코드 포맷팅을 강화하거나, 후처리 단계에서 기본적인 괄호/따옴표 쌍 검사 로직 추가를 고려할 수 있습니다.
---

#### 예시 18

**입력 설명 (src):**
> Reading unicode elements into numpy array

**모델 출력 (pred):**
python
numpy.fromstring('\u0420\u0430\u0430\u0430\u0430\u0430\u0430\u0430\u0430\u0430\u0430\u0430\u0430\u0430\u0430\u0430\u0430\u0430\u0430\u0430\u0430\u0430\u0430\


**오류 메시지:**
> unterminated string literal (detected at line 1) (<string>, line 1)

**분석 및 개선 방향:**

- **원인:** 문장 끝에 괄호나 따옴표가 닫히지 않았거나, 블록이 제대로 끝나지 않음.
- **개선:** 모델 학습 시 일관된 코드 포맷팅을 강화하거나, 후처리 단계에서 기본적인 괄호/따옴표 쌍 검사 로직 추가를 고려할 수 있습니다.
---

### 2.3. 문법 오류 (1건)

#### 예시 11

**입력 설명 (src):**
> How to reverse a dictionary in Python?

**모델 출력 (pred):**
python
dict((k, reverse(v) for k, v in list(d.items()))


**오류 메시지:**
> invalid syntax (<string>, line 1)

**분석 및 개선 방향:**

- **원인:** 파이썬 문법 규칙을 따르지 않은 코드 생성.
- **개선:** 더 많은 양질의 코드 데이터로 학습하거나, 문법 검사기를 이용한 후처리를 적용할 수 있습니다.
---

## 3. 종합 개선 방안

- **데이터 증강:** 다양한 형태의 문법적으로 올바른 코드와 일부러 오류를 포함시킨 코드 쌍을 학습 데이터에 추가하여 모델의 오류 감지 및 수정 능력을 향상시킬 수 있습니다.
- **후처리 파이프라인:** 생성된 코드에 대해 문법 검사(linter)나 정적 분석 도구를 적용하여 흔한 오류 패턴을 자동으로 수정하거나 플래그 지정하는 후처리 단계를 도입하는 것을 고려합니다.
- **모델 아키텍처/ 학습:** 오류 유형별 분포를 분석하여 모델이 특정 유형의 오류를 자주 생성하는 경우, 해당 유형에 취약한 부분을 보완하는 모델 아키텍처 변경이나 학습 전략 수정을 시도할 수 있습니다.
