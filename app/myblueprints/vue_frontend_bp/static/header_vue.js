const HeaderVue = {
    template: /*html*/ `
    <header>
      <nav class="navbar navbar-expand-md navbar-dark bg-dark">
        <div class="container">
          <a class="navbar-brand" href="{{ url_for('index') }}">AUCTION SITE</a>
          <button
            class="navbar-toggler"
            type="button"
            data-toggle="collapse"
            data-target="#navbarsExample04"
            aria-controls="navbarsExample04"
            aria-expanded="false"
            aria-label="Toggle navigation"
          >
            <span class="navbar-toggler-icon"></span>
          </button>

          <div class="collapse navbar-collapse" id="navbarsExample04">
            <ul class="navbar-nav ms-auto align-items-center">
              <li class="nav-item active">
                <a class="nav-link" href="{{ url_for('index') }}"
                  >Home <span class="sr-only">(current)</span></a
                >
              </li>
              <li class="nav-item">
                <a
                  class="nav-link"
                  href="{{ url_for('auctions_bp_sqlalchemy.get_all_auctions') }}"
                  >Auctions</a
                >
              </li>
              <li class="nav-item">
                <a
                  class="nav-link"
                  href="{{ url_for('search_bp.search_items') }}"
                  >Search</a
                >
              </li>
              
                {% if current_user.is_authenticated %}
                <li class="nav-item">
                <a class="nav-link" href="{{ url_for('login_bp.secret') }}">
                  {{ current_user.username }}
                </a>
                </li>
                <li class="nav-item">
                <a type="button"class="btn btn-danger btn-sm my-auto"
                  href="{{ url_for('login_bp.logout') }}">
                  Logout
                </a>
                </li>
                {% else %}
                <a class="nav-link" href="{{ url_for('login_bp.login') }}"
                  >Login</a
                >
                {% endif %}
              </li>
            </ul>
          </div>
        </div>
      </nav>
    </header>
    `};