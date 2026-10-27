import sqlite3

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
)

from database import init_db, get_db_connection


PAGE_SIZE = 12


app = Flask(__name__)

app.secret_key = "my-knowledge-local-secret"

init_db()


@app.context_processor
def inject_sidebar_data():

    connection = get_db_connection()

    categories = connection.execute("""
        SELECT
            categories.id,
            categories.name,
            COUNT(notes.id) AS note_count
        FROM categories
        LEFT JOIN notes
            ON notes.category_id = categories.id
        GROUP BY categories.id
        ORDER BY categories.name COLLATE NOCASE
    """).fetchall()

    total_notes = connection.execute(
        "SELECT COUNT(*) FROM notes"
    ).fetchone()[0]

    connection.close()

    return {
        "sidebar_categories": categories,
        "total_notes": total_notes,
    }


@app.route("/")
def home():

    search_query = request.args.get(
        "q",
        ""
    ).strip()

    category_id = request.args.get(
        "category",
        type=int
    )
    page = max(request.args.get("page", 1, type=int) or 1, 1)

    connection = get_db_connection()

    where_clauses = []
    params = []

    if search_query:

        where_clauses.append("""
            (
                notes.title LIKE ?
                OR notes.content LIKE ?
            )
        """)

        search_term = f"%{search_query}%"

        params.extend([
            search_term,
            search_term,
        ])

    if category_id:

        where_clauses.append(
            "notes.category_id = ?"
        )

        params.append(
            category_id
        )

    where_sql = ""
    if where_clauses:
        where_sql = " WHERE " + " AND ".join(where_clauses)

    total_results = connection.execute(
        "SELECT COUNT(*) FROM notes" + where_sql,
        params
    ).fetchone()[0]
    total_pages = max((total_results + PAGE_SIZE - 1) // PAGE_SIZE, 1)
    page = min(page, total_pages)

    query = """
        SELECT
            notes.*,
            categories.name AS category_name
        FROM notes
        LEFT JOIN categories
            ON notes.category_id = categories.id
    """ + where_sql + """
        ORDER BY
            notes.updated_at DESC,
            notes.created_at DESC
        LIMIT ? OFFSET ?
    """

    notes = connection.execute(
        query,
        [*params, PAGE_SIZE, (page - 1) * PAGE_SIZE]
    ).fetchall()

    active_category = None

    if category_id:

        active_category = connection.execute(
            "SELECT * FROM categories WHERE id = ?",
            (category_id,)
        ).fetchone()

    connection.close()

    return render_template(
        "index.html",
        notes=notes,
        search_query=search_query,
        active_category=active_category,
        page=page,
        total_pages=total_pages,
        total_results=total_results,
    )


@app.route("/add", methods=["GET", "POST"])
def add_note():

    connection = get_db_connection()

    categories = connection.execute("""
        SELECT *
        FROM categories
        ORDER BY name COLLATE NOCASE
    """).fetchall()

    if request.method == "POST":

        title = request.form.get(
            "title",
            ""
        ).strip()

        content = request.form.get(
            "content",
            ""
        ).strip()

        category_id = (
            request.form.get(
                "category_id"
            )
            or None
        )

        if not title:

            flash(
                "Titlul este obligatoriu.",
                "error"
            )

            connection.close()

            return render_template(
                "add.html",
                categories=categories
            )

        if not content:

            flash(
                "Conținutul este obligatoriu.",
                "error"
            )

            connection.close()

            return render_template(
                "add.html",
                categories=categories
            )

        connection.execute("""
            INSERT INTO notes (
                title,
                content,
                category_id
            )
            VALUES (?, ?, ?)
        """, (
            title,
            content,
            category_id
        ))

        connection.commit()

        connection.close()

        flash(
            "Cunoștința a fost salvată.",
            "success"
        )

        return redirect(
            url_for("home")
        )

    connection.close()

    return render_template(
        "add.html",
        categories=categories
    )


@app.route(
    "/edit/<int:note_id>",
    methods=["GET", "POST"]
)
def edit_note(note_id):

    connection = get_db_connection()

    note = connection.execute("""
        SELECT *
        FROM notes
        WHERE id = ?
    """, (note_id,)).fetchone()

    categories = connection.execute("""
        SELECT *
        FROM categories
        ORDER BY name COLLATE NOCASE
    """).fetchall()

    if note is None:

        connection.close()

        return "Cunoștința nu există.", 404

    if request.method == "POST":

        title = request.form.get(
            "title",
            ""
        ).strip()

        content = request.form.get(
            "content",
            ""
        ).strip()

        category_id = (
            request.form.get(
                "category_id"
            )
            or None
        )

        if not title or not content:

            flash(
                "Titlul și conținutul sunt obligatorii.",
                "error"
            )

            connection.close()

            return render_template(
                "edit.html",
                note=note,
                categories=categories
            )

        connection.execute("""
            UPDATE notes
            SET
                title = ?,
                content = ?,
                category_id = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (
            title,
            content,
            category_id,
            note_id
        ))

        connection.commit()

        connection.close()

        flash(
            "Cunoștința a fost actualizată.",
            "success"
        )

        return redirect(
            url_for(
                "view_note",
                note_id=note_id
            )
        )

    connection.close()

    return render_template(
        "edit.html",
        note=note,
        categories=categories
    )


@app.route("/note/<int:note_id>")
def view_note(note_id):

    connection = get_db_connection()

    note = connection.execute("""
        SELECT
            notes.*,
            categories.name AS category_name
        FROM notes
        LEFT JOIN categories
            ON notes.category_id = categories.id
        WHERE notes.id = ?
    """, (note_id,)).fetchone()

    connection.close()

    if note is None:

        return "Cunoștința nu există.", 404

    return render_template(
        "note.html",
        note=note
    )


@app.route(
    "/delete/<int:note_id>",
    methods=["POST"]
)
def delete_note(note_id):

    connection = get_db_connection()

    connection.execute(
        "DELETE FROM notes WHERE id = ?",
        (note_id,)
    )

    connection.commit()

    connection.close()

    flash(
        "Cunoștința a fost ștearsă.",
        "success"
    )

    return redirect(
        url_for("home")
    )


@app.route(
    "/categories/add",
    methods=["POST"]
)
def add_category():

    name = request.form.get(
        "name",
        ""
    ).strip()

    if not name:

        flash(
            "Numele categoriei este obligatoriu.",
            "error"
        )

        return redirect(
            url_for("home")
        )

    connection = get_db_connection()

    try:

        connection.execute(
            """
            INSERT INTO categories (name)
            VALUES (?)
            """,
            (name,)
        )

        connection.commit()

        flash(
            f'Categoria "{name}" a fost creată.',
            "success"
        )

    except sqlite3.IntegrityError:

        flash(
            "Această categorie există deja.",
            "error"
        )

    finally:

        connection.close()

    return redirect(
        url_for("home")
    )


@app.route(
    "/categories/<int:category_id>/delete",
    methods=["POST"]
)
def delete_category(category_id):

    connection = get_db_connection()

    connection.execute("""
        UPDATE notes
        SET category_id = NULL
        WHERE category_id = ?
    """, (category_id,))

    connection.execute(
        "DELETE FROM categories WHERE id = ?",
        (category_id,)
    )

    connection.commit()

    connection.close()

    flash(
        "Categoria a fost ștearsă. Notițele au fost păstrate.",
        "success"
    )

    return redirect(
        url_for("home")
    )


@app.errorhandler(404)
def page_not_found(error):

    return render_template(
        "404.html"
    ), 404


if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True,
        use_reloader=False
    )