/* HeaderBar.jsx */

import { Typography } from '@mui/material';
import SvgIcon from '@mui/material/SvgIcon';
import { ReactComponent as GithubIcon } from './github-logo.svg';
import Grid from '@mui/material/Grid';
import AppBar from '@mui/material/AppBar';

const REPO_URL = 'https://github.com/perintyler/Crypto-Recommendations';

function HeaderBarGrid(props) 
{
    return (
        <Grid container 
          p={2} 
          direction="row" 
          alignItems="center" 
          justifyContent="space-between" 
          sx={{ width: '100%' }}
          backgroundColor="#1d1d1f"
          border={1}
          borderColor="#7F0799"
          {...props}
        />
    )
}

function HeaderBarContainer(props)
{
    return (
        <AppBar
          position="static"
          {...props}
        />
    );
}

export default function HeaderBar()
{
    const websiteTitle = (
        <Typography 
          display="inline" 
          variant="h4" 
          children="CryptoBooks.xyz"
        />
    );

    const githubLogo = (
        <a href={REPO_URL}> 
            <SvgIcon component={GithubIcon} fontSize="large" />
        </a>
    );

    return (
        <HeaderBarContainer>
            <HeaderBarGrid>
                <Grid item xs
                  display="flex" 
                  alignItems="center" 
                  justify="center" 
                  justifyContent="flex-start"
                  children={websiteTitle}
                />
                <Grid item xs 
                  display="flex" 
                  justifyContent="flex-end"
                  children={githubLogo}
                  pt="13px"
                />
            </HeaderBarGrid>
        </HeaderBarContainer>
    );
}

