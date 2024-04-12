package com.backend.admin_server.access_requests.service;

import com.backend.admin_server.access_requests.model.AccessRequestModel;
import com.backend.admin_server.access_requests.repository.AccessRequestRepository;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.List;

@Service
public class AccessRequestService {

    private final AccessRequestRepository accessRequestRepository;

    public AccessRequestService(AccessRequestRepository accessRequestRepository) {
        this.accessRequestRepository = accessRequestRepository;
    }

    public List<AccessRequestModel> getAllSortedByDate() {
        List<AccessRequestModel> requests = new ArrayList<>(accessRequestRepository.findAll());
        requests.sort((r1, r2) -> r2.getDate().compareTo(r1.getDate()));
        return requests;
    }

    public AccessRequestModel get(String requestDate, String requestId) {
        return accessRequestRepository.findByRequestId(requestDate, requestId);
    }
}
