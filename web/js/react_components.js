'use strict';


const serverAddress = "http://localhost:5000";


class App extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            id: null,
            userName: null,
            userType: null,
        };
    }

    render() {
        if (this.state.id == null)
            return this.renderLoginPage();
        else if (this.state.special == "PublishBook")
            return this.renderPublishPage();
        else {
            switch (this.state.userType) {
                case "Reader":
                    return this.renderReaderPage();
                case "Writer":
                    return this.renderWriterPage();
                case "Publisher":
                    return this.renderPublisherPage();
                default:
                    alert("Unknown type!");
            }
        }
    }

    login() {
        const formData = new FormData(document.getElementById("login-form"));
        const userName = formData.get("username");
        const userType = document.getElementById("select-type").value;

        if (userName == '')
            return;
        else {
            switch (userType) {
                case "Reader":
                    fetch(serverAddress + "/get_reader_data?username=" + userName)
                        .then((response) => response.json())
                        .then((json) => 
                            this.setState({
                                id: json.id,
                                userName: userName,
                                userType: userType,

                                ownedBooks: json.owned_books,
                                availableBooks: json.available_books
                            })
                        );
                    break;
                case "Writer":
                    fetch(serverAddress + "/get_writer_data?username=" + userName)
                        .then((response) => response.json())
                        .then((json) => 
                            this.setState({
                                id: json.id,
                                userName: userName,
                                userType: userType,

                                publishedBooks: json.published_books,
                                awaitingBooks: json.awaiting_books,
                                rejectedBooks: json.rejected_books
                            })
                        );
                    break;
                case "Publisher":
                    fetch(serverAddress + "/get_publisher_data?username=" + userName)
                        .then((response) => response.json())
                        .then((json) => 
                            this.setState({
                                id: json.id,
                                userName: userName,
                                userType: userType,

                                awaitingBooks: json.awaiting_books,
                            })
                        );
                    break;
                default:
                    alert("Unknown type!");
            }
        }
    }

    buyBook() {
        const title = document.getElementById("Available").value;

        fetch(serverAddress + "/buy_book?username=" + this.state.userName + "&title=" + title)
            .then((response) => response.json())
            .then((json) => 
                this.setState({
                    ownedBooks: json.owned_books
                })
            );
    }

    publishBook() {
        const title = document.getElementById("title").value;
        const content = document.getElementById("content").value;
        console.log(title + "  " + content);

        fetch(serverAddress + "/publish_book", {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                title: title,
                content: content,
                username: this.state.userName
            })
        });

        var awaitingBooks = this.state.awaitingBooks;
        awaitingBooks.push(title);

        this.setState({
            special: undefined, 
            awaitingBooks: awaitingBooks
        });
    }

    reviewBook(status) {
        const title = document.getElementById("Awaiting").value;
        console.log(title)

        if (status == "Approve")
            fetch(serverAddress + "/accept_book?title=" + title);
        else if (status == "Reject")
            fetch(serverAddress + "/reject_book?title=" + title);

        fetch(serverAddress + "/get_publisher_data?username=" + this.state.userName)
            .then((response) => response.json())
            .then((json) => 
                this.setState({
                    awaitingBooks: json.awaiting_books,
                })
            );
    }

    renderLoginPage() {
        return (
            <div className="masthead d-flex">
                <div className="container text-center my-auto">
                    <h1>Ligature</h1>
                    <h3 style={{ marginBottom: 3 + 'rem' }}>
                        <em>Publishing house & Book store</em>
                    </h3>
                    <select id="select-type">
                        <option value="Reader">Reader</option>
                        <option value="Writer">Writer</option>
                        <option value="Publisher">Publisher</option>
                    </select>
                    <form id="login-form" className="login-form">
                        <input className="input" type="text" name="username" placeholder="Username"></input>
                        <button className="login-form-btn" type="button" onClick={() => this.login()}>Login / Register</button>
                        <div className="flex-col-c"></div>
                    </form>
                </div>
            </div>
        );
    }

    renderReaderPage() {
        return (
            <div className="masthead d-flex">
                <div className="container text-center my-auto">
                    <form>
                        <div className="row h-100">
                            <div className="col-md-6 form-group text-center">
                                <label htmlFor="Bought">Bought Books</label>
                                <select size="5" className="form-control" id="Bought" disabled>
                                if (this.state.ownedBooks.length != 0) {
                                    this.state.ownedBooks.map((book) =>
                                        <option>{book}</option>
                                    )
                                }
                                </select>
                            </div>

                            <div className="col-md-6 form-group text-center">
                                <label htmlFor="Available">Available</label>
                                <select size="5" className="form-control" id="Available">
                                if (this.state.availableBooks.length != 0) {
                                    this.state.availableBooks.map((book) =>
                                        <option>{book}</option>
                                    )
                                }
                                </select>
                            </div>
                        </div>
                        <div className="container-login-form-btn">
                            <button className="login-form-btn"
                                style={{ width: "30%" }}
                                type="button"
                                onClick={() => this.buyBook()}>Buy book</button>
                        </div>
                    </form>
                </div>
            </div>
        );
    }

    renderWriterPage() {
        return (
            <div className="masthead d-flex">
                <div className="container text-center my-auto">
                    <form>
                        <div className="row h-100">
                            <div className="col-md-4 form-group text-center">
                                <label htmlFor="Published">Published</label>
                                <select size="5" className="form-control" id="Published">
                                if (this.state.publishedBooks.length != 0) {
                                    this.state.publishedBooks.map((book) =>
                                        <option>{book}</option>
                                    )
                                }
                                </select>
                            </div>

                            <div className="col-md-4 form-group text-center">
                                <label htmlFor="Awaiting">Awaiting approval</label>
                                <select size="5" className="form-control" id="Awaiting">
                                if (this.state.awaitingBooks.length != 0) {
                                    this.state.awaitingBooks.map((book) =>
                                        <option>{book}</option>
                                    )
                                }
                                </select>
                            </div>

                            <div className="col-md-4 form-group text-center">
                                <label htmlFor="Rejected">Rejected</label>
                                <select size="5" className="form-control" id="Rejected">
                                if (this.state.rejectedBooks.length != 0) {
                                    this.state.rejectedBooks.map((book) =>
                                        <option>{book}</option>
                                    )
                                }
                                </select>
                            </div>
                        </div>
                        <div className="container-login-form-btn">
                            <button className="login-form-btn"
                                style={{ width: "30%" }}
                                type="button"
                                onClick={() => this.setState({special: "PublishBook"})}>Publish book</button>
                        </div>
                    </form>
                </div>
            </div>
        );
    }

    renderPublishPage() {
        return (
            <div className="masthead d-flex">
                <div className="container text-center my-auto">
                    <form className="container-login-from-btn">
                        <input className="input" type="text" id="title" placeholder="Title"></input>
                        <textarea cols="40" rows="3" id="content" placeholder="Content"></textarea>
                        <div className="container-login-form-btn">
                            <button className="login-form-btn"
                                style={{ width: "30%" }}
                                type="button"
                                onClick={() => this.publishBook()}>Publish book</button>
                        </div>
                    </form>
                </div>
            </div>
        )
    }

    renderPublisherPage() {
        return (
            <div className="masthead d-flex">
                <div className="container text-center my-auto">
                    <form>
                        <div className="row h-100">
                            <div className="col-md-12 form-group text-center">
                                <label htmlFor="Awaiting">Publish requests</label>
                                <select size="5" className="form-control" id="Awaiting">
                                if (this.state.awaitingBooks.length != 0) {
                                    this.state.awaitingBooks.map((book) =>
                                        <option>{book}</option>
                                    )
                                }
                                </select>
                            </div>
                        </div>
                        <div className="row h-100">
                            <div className="col-md-6 container-login-form-btn">
                                <button className="login-form-btn"
                                    id="Approve"
                                    style={{ width: "50%" }}
                                    type="button"
                                    onClick={() => this.reviewBook("Approve")}>Approve</button>
                            </div>
                            <div className="col-md-6 container-login-form-btn">
                                <button className="login-form-btn"
                                    id="Reject"
                                    style={{ width: "50%" }}
                                    type="button"
                                    onClick={() => this.reviewBook("Reject")}>Reject</button>
                            </div>
                        </div>
                    </form>
                </div>
            </div>
        );
    }
}


ReactDOM.render(
    <App />,
    document.getElementById('SPA')
);
