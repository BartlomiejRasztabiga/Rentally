import React from 'react';
import PropTypes from 'prop-types';
import clsx from 'clsx';
import {
  Box,
  Card,
  CardContent,
  Divider,
  Grid,
  makeStyles,
  Typography
} from '@material-ui/core';
import Image from 'material-ui-image';

const useStyles = makeStyles((theme) => ({
  root: {
    display: 'flex',
    flexDirection: 'column'
  },
  statsItem: {
    alignItems: 'center',
    display: 'flex'
  },
  statsIcon: {
    marginRight: theme.spacing(1)
  },
  large: {
    width: theme.spacing(20),
    height: theme.spacing(20)
  }
}));

const CarCard = ({ className, product, ...rest }) => {
  const classes = useStyles();

  return (
    <Card className={clsx(classes.root, className)} {...rest}>
      <CardContent>
        <Box display="flex" justifyContent="center" mb={3}>
          <Image src={product.media} />
        </Box>
        <Typography align="left" color="textPrimary" gutterBottom variant="h4">
          {product.modelName}
        </Typography>
        <Typography align="center" color="textPrimary" variant="body1">
          {product.description}
        </Typography>
      </CardContent>
      <Box flexGrow={1} />
      <Divider />
      <Box p={2}>
        <Grid container justify="space-between" spacing={2}>
          <Grid className={classes.statsItem} item>
            test
          </Grid>
        </Grid>
      </Box>
    </Card>
  );
};

CarCard.propTypes = {
  className: PropTypes.string,
  product: PropTypes.object.isRequired
};

export default CarCard;
