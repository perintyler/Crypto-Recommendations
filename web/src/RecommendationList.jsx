/* RecommendationList.jsx */

import React from "react";
import { Typography } from '@mui/material';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Box from '@mui/material/Box';

const COLORS = ['#f44336', '#673ab7', '#2196f3', '#00bcd4', '#cddc39']

function RecommendationListItem({ recommendation, index })
{

    const recommendationLabel = (
        <Typography 
          fontSize="18px" 
          marginLeft={1.5} 
          marginBottom="5px" 
          color="white"
          sx={{textDecoration: 'underline'}}
          children={`Recommendation #${index+1}`}
        />
    );

    const recommendationCard = (
        <Card style={{borderRadius: "20px", backgroundColor: COLORS[index]}}>
            <CardContent>
                <Typography style={{color: 'white', paddingTop: '6px'}} variant="body1">
                    &nbsp; <b>{recommendation}</b>
                </Typography>
            </CardContent>
        </Card>
    );

    return <li><Box paddingBottom={3}>{recommendationLabel}{recommendationCard}</Box></li>;
}

export default function RecommendationList({ recommendations })
{
    const listItems = recommendations.map(
        (rec, index) => <RecommendationListItem recommendation={rec} key={index} index={index} />
    );
    return <ul id='rec-list'>{listItems}</ul>;
}


