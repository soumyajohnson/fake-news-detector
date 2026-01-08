package com.example.fakenews.exception;

import com.example.fakenews.dto.ErrorResponse;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.authentication.BadCredentialsException;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ControllerAdvice;
import org.springframework.web.bind.annotation.ExceptionHandler;

import java.util.stream.Collectors;

@ControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(BadCredentialsException.class)
    public ResponseEntity<ErrorResponse> handleBadCredentials(BadCredentialsException ex) {
        return new ResponseEntity<>(
            new ErrorResponse("AUTH_ERROR", ex.getMessage()),
            HttpStatus.UNAUTHORIZED
        );
    }

    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<ErrorResponse> handleValidationErrors(MethodArgumentNotValidException ex) {
        String errors = ex.getBindingResult().getFieldErrors().stream()
                .map(err -> err.getField() + ": " + err.getDefaultMessage())
                .collect(Collectors.joining(", "));
        return new ResponseEntity<>(
            new ErrorResponse("VALIDATION_ERROR", errors),
            HttpStatus.BAD_REQUEST
        );
    }

    @ExceptionHandler(RuntimeException.class)
    public ResponseEntity<ErrorResponse> handleRuntimeException(RuntimeException ex) {
        if (ex.getMessage() != null && ex.getMessage().contains("ML service not reachable")) {
             return new ResponseEntity<>(
                 new ErrorResponse("ML_SERVICE_UNAVAILABLE", "ML service not reachable"),
                 HttpStatus.SERVICE_UNAVAILABLE
             );
        }
        if (ex.getMessage() != null && ex.getMessage().contains("Email already exists")) {
            return new ResponseEntity<>(
                new ErrorResponse("DUPLICATE_EMAIL", ex.getMessage()),
                HttpStatus.BAD_REQUEST
            );
        }
        
        return new ResponseEntity<>(
            new ErrorResponse("INTERNAL_SERVER_ERROR", ex.getMessage()),
            HttpStatus.INTERNAL_SERVER_ERROR
        );
    }
}
