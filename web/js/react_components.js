'use strict';

class MainScreen extends React.Component {
    render() {
        return (
            <div className="masthead d-flex">
                <div className="container text-center my-auto">
                    <h1 className="mb-1">Ligature</h1>
                    <h3 className="mb-5">
                        <em>Publishing house & Book store</em>
                    </h3>
                    <a className="btn btn-primary btn-xl js-scroll-trigger"
                        data-toggle="modal" data-target="#LoginForm">Login</a>
                </div>
                <div className="overlay"></div>
            </div>
        )
    }
}

ReactDOM.render(
    <MainScreen />,
    document.getElementById('SPA')
);
