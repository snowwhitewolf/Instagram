# 인스타 클론 코딩 프로젝트

### 목표

* 실제 인스타그램과 유사한 디자인
* 회원가입 및 로그인 기능
* 피드 목록 및 상세 페이지 구현
* 프로필 이미지 변경
* 비밀번호 및 회원정보 변경



## 1. 회원가입

![](README.assets/image-20211020185004777.png)



* 인스타그램과 유사하게 페이지를 디자인 하였다.
* user model에 대한 이해가 부족하여 기존의 form을 그대로 사용하였다.
* 이로 인해 작성 form에 디테일이 부족했다.
* 새롭게 배운 방법으로 user model을 사용할 수 있도록 노력해야겠다.



```python
def signup(request):
    if request.user.is_authenticated:
        return redirect('feeds:index')

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('feeds:index')
    else:
        form = CustomUserCreationForm()
    context = {
        'form': form
    }
    return render(request, 'accounts/signup.html', context)
```



## 2. 로그인

![image-20211020185022519](README.assets/image-20211020185022519.png)



* 로그인 페이지는 디테일에 좀 더 신경을 많이 썼다.
* 회원가입 페이지와 마찬가지로 라벨태그를 못 지워서 아쉬웠다.
* 제일 마음에 드는 페이지이다.



```python
def login(request):
    if request.user.is_authenticated:
        return redirect('feeds:index')

    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect(request.GET.get('next') or 'feeds:index')
    else:
        form = AuthenticationForm()
    
    context = {
        'form': form 
    }
    return render(request, 'accounts/login.html', context)
```



## 3. 네비게이션 바

![image-20211020185429182](README.assets/image-20211020185429182.png)

![image-20211020185441156](README.assets/image-20211020185441156.png)



* 가장 자신있는 파트였기 때문에 재밌게 작업하였다.
* 네비게이션 바에 대한 이해도가 많이 상승하였다.
* 페이지 이동 시 아이콘이 바뀌는 것을 구현해보고 싶다.



```html
{% if request.user.is_authenticated %}
  <nav class="sticky-top navbar navbar-expand-lg bg-white border-bottom" style = "height : 50px; margin-left:60px">
      <div class="container-fluid ">
      <a href="{% url 'feeds:index' %}" style = "margin-left : 350px; margin-right : 200px">
      <img src="{% static 'logo.png' %}" alt="" class ="navbar-brand my-auto">
      </a>
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav ">
    <form class="d-flex my-auto" style = "height : 30px; ">
      <input class="form-control mx-5 text-center" type="search" placeholder="검색" aria-label="Search" style="background-color:#fafafa">
  
    </form>
    <li class="nav-item my-auto " style = "margin-left : 100px; ">
      <a class="nav-link active" aria-current="page" href="{% url 'feeds:index' %}"><img src="{% static 'nav_home.png' %}" alt=""></a>
    </li>
    <li class="nav-item my-auto">
      <a class="nav-link active" aria-current="page" href="#"><img src="{% static 'nav_dm.png' %}" alt=""></a>
    </li>
    <li class="nav-item my-auto">
      <a class="nav-link active" aria-current="page" href="#"><img src="{% static 'nav_search.png' %}" alt=""></a>
    </li>
    <li class="nav-item dropdown text-nowrap my-auto">
    <a class="nav-link" data-bs-toggle="dropdown" href="#" role="button" aria-expanded="false">
    <img src="{% static 'nav_like.png' %}" alt="" href="#"></a>
    <ul class="dropdown-menu text-center my-auto">
    <img src="{% static 'nav_like_in.png' %}" alt="">
      <p>게시물 활동</p>
      <p>다른 사람이 회원님의 게시물을 좋아하거나 댓글을 남기면 여기에 표시됩니다.</p>
    </ul>
  </li>
    <li class="nav-item dropdown my-auto">
    <a class="nav-link my-auto" data-bs-toggle="dropdown" href="#" role="button" aria-expanded="false">
    {% if user.profile_image %}
    <img src="{{ user.profile_image.url }}" alt="" style="width:22px; height:22px; border-radius: 70%;" href="#">
    {% else %}
    <img src="{% static '프로필.jpg' %}" alt="" style="width:22px; height:22px; border-radius: 70%;" href="#">
    {% endif %}
    </a>
    <ul class="dropdown-menu">
      <li><a class="dropdown-item" href="#">프로필</a></li>
      <li><a class="dropdown-item" href="#">저장됨</a></li>
      <li><a class="dropdown-item" href="{% url 'accounts:edit' %}">설정</a></li>
      <li><a class="dropdown-item" href="#">계정 전환</a></li>
      <li><hr class="dropdown-divider"></li>
      
      <li
      >{% if request.user.is_authenticated %}
      <form action="{% url 'accounts:logout' %}"method="POST">
      {% csrf_token %}
      <button class="btn btn-white">로그아웃</button>
      </form>
  {% endif %}</li>
    </ul>
  </li>
        </ul>
      </div>
    </div>
  </nav>
  {% else %}
  {% endif %}

```



## 4. 피드

![image-20211020185412935](README.assets/image-20211020185412935.png)

![image-20211020185556284](README.assets/image-20211020185556284.png)



* 페이지 구조 및 디테일에 많이 신경썼다.
* 구현하지 못한 기능들이 많아서 아쉬움이 남았다.



```html
{% extends 'base.html' %}
{% load static %}
{% block content %}
<div class="row" style="margin-left : 100px; margin-top : 20px;">
<div class="col-8">
{% for feed in feeds %}
<br>
<div class="card" style="width: 38rem; ">
<p class="p-0 m-3" style = "font-weight: 600; ">

{% if user.profile_image %}
<img src="{{ user.profile_image.url }}" alt="" style="width:30px; height:30px; border-radius: 70%; margin-right : 10px;" href="#">
{% else %}
<img src="{% static '프로필.jpg' %}" alt="" style="width:30px; height:30px; border-radius: 70%; margin-right : 10px;" href="#">
{% endif %}
  {{user}}
  <a>
  <button type="button" class="btn btn-white p-0" data-bs-toggle="modal" data-bs-target="#exampleModal" style="width:30px; height:30px; margin-left:480px;">
  <img src="{% static '....png' %}" alt="">
</button>
</a>
</p>

<div class="modal fade" id="exampleModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
  <div class="modal-dialog modal-dialog-centered">
    <div class="modal-content">
      <div class="modal-body text-center">
        <form action="{% url 'feeds:delete' feed.pk %}"method="POST">
{% csrf_token %}
<button class="btn btn-white text-danger">삭제</button>
</form>
<hr>
<button href="{% url 'feeds:detail' feed.pk %}" class="btn btn-white"><a href="{% url 'feeds:detail' feed.pk %}" class="text-decoration-none text-dark">게시물로 이동</a></button>
<hr>
<button type="button" class="btn btn-white " data-bs-dismiss="modal">취소</button>
      </div>
    </div>
  </div>
</div>
  <img src="{{ feed.image.url }}" class="card-img-top" alt="..." >
  <div class="card-body">
  <img class = "card-title" src="{% static 'feed_like.png' %}" alt="" style="width:30px; height:30px;">
  <img class = "card-title" src="{% static 'feed_chat.png' %}" alt="" style="width:30px; height:30px;">
  <img class = "card-title" src="{% static 'feed_dm.png' %}" alt="" style="width:30px; height:30px;">
  <img class = "card-title" src="{% static 'feed_fix.png' %}" alt="" style="width:30px; height:30px; margin-left: 435px">
    <p class="card-text" style="font-size: 15px; font-weight:600;">{{user}} <span style ="font-weight:400;">{{ feed.content }}</span></p>
    <p class="card-text" style="color: #c7c7c7; font-size: 10px;">{{feed.created_at|date:'n월 j일'}}</p>
  </div>
</div>

{% empty %}
{% endfor %}

<div class="col-4" style = "position : fixed; top: 100px;left: 1100px; width:350px;">
<p style = "font-weight: 600;">
{% if user.profile_image %}
<img src="{{ user.profile_image.url }}" alt="" style="width:56px; height:56px; border-radius: 70%; margin-right : 10px;" href="#">
{% else %}
<img src="{% static '프로필.jpg' %}" alt="" style="width:56px; height:56px; border-radius: 70%; margin-right : 10px;" href="#">
{% endif %}
  {{user}}
  <a href="" class="text-decoration-none" style="font-size: 12px; margin-left:180px">전환</a>
</p>
<img src="{% static 'reco.png' %}" alt="..." style="margin-bottom : 20px;" >
<br>
<div>
<a href="" class="text-decoration-none" style="color: #c7c7c7; font-size: 11px;">소개</a>
<span style="color: #c7c7c7; font-size: 11px;">·</span>
<a href="" class="text-decoration-none"style="color: #c7c7c7; font-size: 11px;">도움말</a>
<span style="color: #c7c7c7; font-size: 11px;">·</span>
<a href="" class="text-decoration-none "style="color: #c7c7c7;font-size: 11px;">홍보 센터</a>
<span style="color: #c7c7c7; font-size: 11px;">·</span>
<a href="" class="text-decoration-none "style="color: #c7c7c7;font-size: 11px;">API</a>
<span style="color: #c7c7c7; font-size: 11px;">·</span>
<a href="" class="text-decoration-none"style="color: #c7c7c7;font-size: 11px;">채용 정보</a>
<span style="color: #c7c7c7; font-size: 11px;">·</span>
<br>
<a href="" class="text-decoration-none"style="color: #c7c7c7;font-size: 11px;">개인정보처리방침</a>
<span style="color: #c7c7c7; font-size: 11px;">·</span>
<a href="" class="text-decoration-none"style="color: #c7c7c7;font-size: 11px;">약관</a>
<span style="color: #c7c7c7; font-size: 11px;">·</span>
<a href="" class="text-decoration-none "style="color: #c7c7c7;font-size: 11px;">위치</a>
<span style="color: #c7c7c7; font-size: 11px;">·</span>
<a href="" class="text-decoration-none"style="color: #c7c7c7;font-size: 11px;">인기 계정</a>
<span style="color: #c7c7c7; font-size: 11px;">·</span>
<a href="" class="text-decoration-none"style="color: #c7c7c7;font-size: 11px;">해시태그</a>
<span style="color: #c7c7c7; font-size: 11px;">·</span>
<a href="" class="text-decoration-none"style="color: #c7c7c7;font-size: 11px;">언어</a>
<br>
<div style="padding-top : 20px;">
<p style="color: #c7c7c7;font-size: 11px;">© 2021 Instagram from Facebook</p>
</div>
</div>
</div>
{% endblock content %}
```



## 5. 피드 디테일

![image-20211020185635410](README.assets/image-20211020185635410.png)



* 역시 수정할 부분이 많은 페이지이다.
* 시간 부족으로 인해 거의 구현하지 못했다.



```html
{% extends 'base.html' %}
{% load static %}
{% block content %}
<div class="container">
<div class="row" style = "margin-top : 100px;">
<div class="col">
<div class="card" style="width: 30rem; background-color:#fafafa; margin-left : 130px;">
<img src="{{ feed.image.url }}" class="card-img-top" alt="..." >
</div>
</div>
<div class="col  border bg-white">
{% if user.profile_image %}
<img src="{{ user.profile_image.url }}" alt="" style="width:30px; height:30px; border-radius: 70%; margin-right : 10px;" href="#">
{% else %}
<img src="{% static '프로필.jpg' %}" alt="" style="width:30px; height:30px; border-radius: 70%; margin-right : 10px;" href="#">
{% endif %}
  {{user}}
  <button type="button" style="margin-left:510px" class="btn btn-white" data-bs-toggle="modal" data-bs-target="#exampleModal">
  <img src="{% static '....png' %}" alt="">
</button>
</p>
<hr>
<div class="modal fade" id="exampleModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
  <div class="modal-dialog modal-dialog-centered">
    <div class="modal-content">
      <div class="modal-body text-center">
        <form action="{% url 'feeds:delete' feed.pk %}"method="POST">
{% csrf_token %}
<button class="btn btn-white text-danger">삭제</button>
</form>
<hr>
<button type="button" class="btn btn-white " data-bs-dismiss="modal">취소</button>
      </div>
    </div>
  </div>
</div>
  <div>
  <h5>{{user}} {{feed.context}}</h5>
  </div>
  <div>
  <img  src="{% static 'nav_like.png' %}" alt="" style="width:30px; height:30px;">
  <img  src="{% static 'feed_chat.png' %}" alt="" style="width:30px; height:30px;">
  <img  src="{% static 'nav_dm.png' %}" alt="" style="width:30px; height:30px;">
  <img  src="{% static 'feed_fix.png' %}" alt="" style="width:30px; height:30px;">
    <p class="card-text text-secondary">{{feed.created_at|date:'n월 j일'}}</p>
  </div>
</div>
</div>
</div>
{% endblock content %}
```



## 6. 설정

![image-20211020185454441](README.assets/image-20211020185454441.png)

![image-20211020185501555](README.assets/image-20211020185501555.png)



* 가장 마지막에 작업했던 페이지이다.
* 프로필 편집과 비밀번호 변경만 구현해서 아쉬웠다.



# 마무리

* 첫번째 프로젝트여서 만족감 보단 아쉬움이 더 많이 남았지만 조금은 성장한 것 같다.
* 페이지 구성과 db관리를 좀 더 공부해야겠다.
* 좀 더 완성된 프로젝트에 도전하고 싶다.

