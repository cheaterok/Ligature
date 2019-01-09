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
            fetch(serverAddress + "/login?username=" + userName)
                .then((response) => response.json())
                .then((json) =>
                    this.setState({
                        id: json.id,
                        userName: json.name,
                        userType: userType
                    })
                );
        }
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
                                <select size="5" className="form-control" id="Bought">
                                    <option>First item</option>
                                    <option>Second item</option>
                                    <option>Third item</option>
                                </select>
                            </div>

                            <div className="col-md-6 form-group text-center">
                                <label htmlFor="Available">Available</label>
                                <select size="5" className="form-control" id="Available">
                                    <option>First item</option>
                                    <option>Second item</option>
                                    <option>Third item</option>
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
                                    <option>First item</option>
                                    <option>Second item</option>
                                    <option>Third item</option>
                                </select>
                            </div>

                            <div className="col-md-4 form-group text-center">
                                <label htmlFor="Awaiting">Awaiting approval</label>
                                <select size="5" className="form-control" id="Awaiting">
                                    <option>First item</option>
                                    <option>Second item</option>
                                    <option>Third item</option>
                                </select>
                            </div>

                            <div className="col-md-4 form-group text-center">
                                <label htmlFor="Rejected">Rejected</label>
                                <select size="5" className="form-control" id="Rejected">
                                    <option>First item</option>
                                    <option>Second item</option>
                                    <option>Third item</option>
                                </select>
                            </div>
                        </div>
                        <div className="container-login-form-btn">
                            <button className="login-form-btn"
                                style={{ width: "30%" }}
                                type="button"
                                onClick={() => this.publishBook()}>Publish book</button>
                        </div>
                    </form>
                </div>
            </div>
        );
    }

    renderPublisherPage() {
        return (
            <div className="masthead d-flex">
                <div className="container text-center my-auto">
                    <form>
                        <div className="row h-100">
                            <div className="col-md-12 form-group text-center">
                                <label htmlFor="Published">Published</label>
                                <select size="5" className="form-control" id="Published">
                                    <option>First item</option>
                                    <option>Second item</option>
                                    <option>Third item</option>
                                </select>
                            </div>
                        </div>
                        <div className="row h-100">
                            <div className="col-md-6 container-login-form-btn">
                                <button className="login-form-btn"
                                    style={{ width: "50%" }}
                                    type="button"
                                    onClick={() => this.publishBook()}>Publish book</button>
                            </div>
                            <div className="col-md-6 container-login-form-btn">
                                <button className="login-form-btn"
                                    style={{ width: "50%" }}
                                    type="button"
                                    onClick={() => this.publishBook()}>Publish book</button>
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
