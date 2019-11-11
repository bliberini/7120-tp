import React, { Component } from 'react';
import CssBaseline from '@material-ui/core/CssBaseline';
import Typography from '@material-ui/core/Typography';
import { withStyles } from '@material-ui/core/styles';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import IconButton from '@material-ui/core/IconButton';
import MenuIcon from '@material-ui/icons/Menu';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import Paper from '@material-ui/core/Paper';
import Grid from '@material-ui/core/Grid';
import Button from '@material-ui/core/Button';
import TextField from '@material-ui/core/TextField';
import ErrorIcon from '@material-ui/icons/Error';
import CloseIcon from '@material-ui/icons/Close';
import Snackbar from '@material-ui/core/Snackbar';
import SnackbarContent from '@material-ui/core/SnackbarContent';
import './App.css';
import { BeatLoader } from 'react-spinners';
import axios from 'axios';

const useStyles = theme => ({
  root: {
    flexGrow: 1,
    width: '100%',
    overflowX: 'hidden',
  },
  menuButton: {
    marginRight: theme.spacing(2),
  },
  title: {
    flexGrow: 1,
  },
  table: {
    minWidth: 650,
  },
  paper: {
    padding: theme.spacing(1),
    textAlign: 'center',
    color: theme.palette.text.secondary,
  },
  grid: {
    padding: theme.spacing(1),
    overflow: 'hidden',
  },
  textField: {
    marginLeft: theme.spacing(1),
    marginRight: theme.spacing(1),
    width: 200,
  },
  button: {
    margin: theme.spacing(1),
    marginTop: theme.spacing(3),
  },
  error: {
    backgroundColor: theme.palette.error.dark,
  },
  icon: {
    fontSize: 20,
  },
  iconVariant: {
    opacity: 0.9,
    marginRight: theme.spacing(1),
  },
  message: {
    display: 'flex',
    alignItems: 'center',
  },
});

function createData(name, roi, std) {
  return { name, roi: roi * 100, std: std * 100, pct: '' };
}

class App extends Component {

  constructor() {
    super();
    this.state = {
      maxRisk: 0,
      loading: false,
      return: '',
      rows: [
        createData('Apple', -0.0322773, 0.01811),
        createData('General Motors', -0.13283933, Math.sqrt(0.000407)),
        createData('Microsoft', 0.22378075, Math.sqrt(0.000318)),
        createData('Tesla', 0.20444404, 0.001363),
        createData('Spotify', -0.27523063, 0.000691),
        createData('Bank of America', 0.28569167, 0.000843),
        createData('Coca-Cola Company', 0.08414536, 0.000089),
      ]
    };

    this.onClick = this.onClick.bind(this);
    this.onChange = this.onChange.bind(this);
  }
  onClick() {
    this.setState({ loading: true });
    axios.post('http://localhost:5000/generate', { max_risk: this.state.maxRisk }, { headers: {
      'Access-Control-Allow-Origin': '*',
      'Content-Type': 'application/json',
    }})
      .then((response) => {
        const rows = this.state.rows.slice();
        for (let i = 0; i < this.state.rows.length; i++) {
          rows[i].pct = Math.round(response.data.weights[i] * 100 * 10000) / 10000 + '%';
        }
        this.setState({
          rows,
          loading: false,
          return: response.data.expected_return
        });
      })
      .catch((error) => {
        console.log("There was an error")
        console.log(error)
        this.setState({ loading: false, error: true });
      });
  }

  onChange(event) {
    this.setState({ maxRisk: event.target.value });
  }

  render() {
    const classes = this.props.classes;
    return (
      <div className={classes.root}>
        <AppBar position="static">
          <Toolbar>
            <IconButton edge="start" className={classes.menuButton} color="inherit" aria-label="menu">
              <MenuIcon />
            </IconButton>
            <Typography variant="h6" className={classes.title}>
              PO'N'GA - Portfolio Optimization And Genetic Algorithms
            </Typography>
          </Toolbar>
        </AppBar>
        <Grid className={classes.grid} container spacing={3} alignItems="center" alignContent="center" justify="center">
          <CssBaseline />
          <Grid item xs={10} justify="center">
            <form style={{ display: 'flex', flexWrap: 'wrap', }} noValidate autoComplete="off">
              <div>
                <TextField
                  id="standard-required"
                  label="Riesgo máximo (%)"
                  className={classes.textField}
                  margin="normal"
                  onChange={this.onChange}
                  disabled={this.state.loading}
                />
                <TextField
                  disabled
                  id="standard-disabled"
                  label="Retorno de inversión"
                  className={classes.textField}
                  margin="normal"
                  value={this.state.return === '' ? '' : (Math.round(this.state.return * 100) / 100 + '%')}
                />
                <Button
                  variant="contained"
                  className={classes.button}
                  onClick={this.onClick}
                  disabled={this.state.loading}
                >
                  Generar
                </Button>
              </div>
            </form>
          </Grid>
          <Grid item xs={10}>
            <Paper className={classes.paper}>
              <Table className={classes.table} aria-label="simple table">
                <TableHead>
                  <TableRow>
                    <TableCell style={{ backgroundColor: "black", color: "white", fontWeight: "bolder" }}>Activo</TableCell>
                    <TableCell style={{ backgroundColor: "black", color: "white", fontWeight: "bolder" }} align="right">Retorno</TableCell>
                    <TableCell style={{ backgroundColor: "black", color: "white", fontWeight: "bolder" }} align="right">Riesgo</TableCell>
                    <TableCell style={{ backgroundColor: "black", color: "white", fontWeight: "bolder" }} align="right">% Portfolio</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {this.state.rows.map(row => (
                    <TableRow key={row.name}>
                      <TableCell component="th" scope="row">
                        {row.name}
                      </TableCell>
                      <TableCell align="right">{Math.round(row.roi * 100) / 100}%</TableCell>
                      <TableCell align="right">{Math.round(row.std * 10000) / 10000}%</TableCell>
                      <TableCell align="right">
                        {
                          this.state.loading ?
                            <BeatLoader
                              sizeUnit={"px"}
                              size={15}
                              color={'#000000'}
                              loading={this.state.loading}
                            />
                            :
                            row.pct
                        }
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </Paper>
          </Grid>
        </Grid>
        {
          this.state.error ?
            <Snackbar
              anchorOrigin={{
                vertical: 'bottom',
                horizontal: 'left',
              }}
              open={this.state.error}
              autoHideDuration={3000}
              onClose={() => { this.setState({ error: false }) }}
            >
              <SnackbarContent
                className={classes.error}
                aria-describedby="client-snackbar"
                message={
                  <span id="client-snackbar" className={classes.message}>
                    <ErrorIcon />
                    No se pudo generar portfolio con el riesgo máximo pedido
                  </span>
                }
                action={[
                  <IconButton key="close" aria-label="close" color="inherit" onClick={() => { this.setState({ error: false }) }}>
                    <CloseIcon className={classes.icon} />
                  </IconButton>,
                ]}
              />
            </Snackbar>
            :
            <React.Fragment />
        }
      </div>
    );
  }
}

export default withStyles(useStyles)(App);;
