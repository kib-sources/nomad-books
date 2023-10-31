package com.dromakin.serverauth.config.security;

import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.web.filter.GenericFilterBean;

import javax.servlet.FilterChain;
import javax.servlet.ServletException;
import javax.servlet.ServletRequest;
import javax.servlet.ServletResponse;
import javax.servlet.http.HttpServletRequest;
import java.io.IOException;

public class JWTFilter extends GenericFilterBean {

    private JWTAuthServer jwtAuthServer;

    public JWTFilter(JWTAuthServer jwtAuthServer) {
        this.jwtAuthServer = jwtAuthServer;
    }

    @Override
    public void doFilter(ServletRequest servletRequest, ServletResponse servletResponse, FilterChain filterChain) throws IOException, ServletException {
        String token = jwtAuthServer.resolveToken((HttpServletRequest) servletRequest);
        if (token != null && jwtAuthServer.validateToken(token)) {
            Authentication authentication = jwtAuthServer.getAuthentication(token);
            if (authentication != null) {
                SecurityContextHolder.getContext().setAuthentication(authentication);
            }
        }
        filterChain.doFilter(servletRequest, servletResponse);
    }
}
